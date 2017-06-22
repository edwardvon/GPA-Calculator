# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.db import connection,Error
from .models import Major,Detail,Score

# Create your views here.
fuck_thisname = ''

def index(request):
    result_list = []
    result_list = Major.objects.get_with_value('college','信息工程学院')
    context = {
        'result_list': result_list
    }
    return render(request, 'Page1.html', context)

def detail(request,stu_num):
    global fuck_thisname
    # result_list = Score.objects.get_with_value('stu_num', int(stu_num))
    result_list = get_view(stu_num)
    range1 = {1:'公共必修课程',2:'专业核心课程',3:'专业选修课程'}
    context = {
        'result_list': result_list,
        'range': range1,
        'name': fuck_thisname,
    }
    return render(request, 'detail.html', context)


def submit(request):
    global fuck_thisname
    gpa_content = request.POST['content']
    gpa_content = gpa_content.replace(' level','level').replace(':','\t').replace('\t',' ')
    gpa_content = gpa_content.split(' ')
    try:
        index = gpa_content.index('姓名')
    except ValueError:
        return render(request, 'Page1.html', {'error_message': "把下面这串内容截图给我！",
                                              'gpa_content': gpa_content})
    stu_number = gpa_content[index-1]
    fuck_thisname = gpa_content[index+1]
    stu_class_name = gpa_content[index+5].split(' ')[0]
    major_num = Major.objects.get_with_value('name',stu_class_name,'year',stu_number[0:4])[0].number
    # lesson_list = Detail.objects.get_with_value('class_num', int(result_list[0].number))
    view_create(stu_number,major_num)
    result_list = spilt_by_term(gpa_content, stu_number)
    score_insert(result_list,stu_number,major_num)
    return HttpResponseRedirect(reverse('counter:detail', args=(stu_number,)))

def result(request,stu_num):
    pass


#将分割成列表的成绩表以学期为单位分割
def spilt_by_term(content_list, item):
    result_list = []
    all_point = [i for i, j in enumerate(content_list) if j == item]
    all_point.append(int(-1))
    for i in range(len(all_point)-1):
        a = all_point[i]
        b = all_point[i+1]
        result_list.append(content_list[a:b])
    for i in range(len(result_list)):
        start = result_list[i].index('备注')
        for x in range(0,10):
            if result_list[i][start+x]=='1':
                start = start + x
                break
        try:
            end = result_list[i].index('所选学分')
        except ValueError:
            end = result_list[i].index('取得学分')-2
        result_list[i] = result_list[i][start:end]
    lesson_single = []
    for term in result_list:
        for i in range((len(term)+1)//11):
            a = term[i*11:(i+1)*11]
            lesson_single.append(a[:-1])
    return lesson_single
#
def score_insert(list,stu_num,class_num):
    for item in list:
        a = item[1:]
        a.append(str(stu_num))
        a.append(str(class_num))
        Score.objects.score_init(a)
    return 1

def view_create(stu_num, class_num):
    with connection.cursor() as cursor:
        cursor.execute("DROP VIEW IF EXISTS %s"%('view'+str(stu_num)))
        try:
            cursor.execute("CREATE VIEW %s AS SELECT * FROM counter_detail WHERE CLASS_NUM=%s;"%('view'+str(stu_num),str(class_num)))
        except Error as err:
            print(err)
        return 1

def get_view(stu_num):
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM %s"%('view'+str(stu_num)))
        except Error as err:
            print(err)
        result_list = []
        for row in cursor.fetchall():
            p = Detail.objects.model(id=row[0], number=row[1], name=row[2], point=row[3], type=row[4], class_num=row[5])
            result_list.append(p)
    return result_list