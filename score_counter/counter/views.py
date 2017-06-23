# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.db import connection,Error
from .models import Major,Detail,Score,MajorScore
import json

# Create your views here.
stu_name = ''

def index(request):
    return render(request, 'Page1.html')

def submit(request):
    global stu_name
    #成绩单内容获取，并分割，内容中主要存在空格和制表符\t
    gpa_content = request.POST['content']
    #大学英语中“A level”的空格会影响分割
    gpa_content = gpa_content.replace(' level','level').replace(':','\t').replace('\t',' ')
    gpa_content = gpa_content.split(' ')
    #粗略判断内容是否为成绩表，否则提示error
    try:
        index = gpa_content.index('绩点')
        index = gpa_content.index('姓名')
    except ValueError:
        return render(request, 'Page1.html', {'error_message': "同学！你是不是复制错了？看看说明吧",
                                              'gpa_content':gpa_content,})
    stu_number = gpa_content[index-1]
    stu_name = gpa_content[index+1]
    stu_class_name = gpa_content[index+5]
    major = Major.objects.filter(name=stu_class_name,year=stu_number[0:4])[0]
    #成绩单内容以学期分割
    result_list = spilt_by_term(gpa_content, stu_number)
    #课程条目插入数据库
    score_insert(result_list,stu_number,major.number)
    return HttpResponseRedirect(reverse('counter:detail', args=(stu_number,)))

def detail(request,stu_num):
    global stu_name
    stu_num = int(stu_num)
    stu_class_num = Score.objects.filter(stu_num=stu_num)[0].class_num
    major = Major.objects.get(number=stu_class_num)
    MajorScore.objects.majorscore_init(stu_num,stu_class_num)
    result_list = MajorScore.objects.filter(stu_num=stu_num)
    range1 = {1:'公共必修课程',2:'专业核心课程',3:'专业选修课程'}
    context = {
        'result_list': result_list,
        'range': range1,
        'name': stu_name,
        'score_request': major,
        'stu_number':stu_num,
    }
    return render(request, 'detail.html', context)

def result(request,stu_num):
    MajorScore.objects.majorscore_join(stu_num)
    result_list = MajorScore.objects.filter(stu_num=stu_num,type__lte=2)
    score_request = Major.objects.get_scorerequest(result_list[0].class_num)
    sele_list = Score.objects.filter(type=3,stu_num=stu_num)
    sele_total = sum(i.get_point for i in sele_list)
    gpa = Score.objects.get_gpa(stu_num)
    context={
        'name': stu_name,
        'result_list': result_list,
        'range': {1:'公共必修课程',2:'专业核心课程'},
        'sele_list':sele_list,
        'score_request': score_request,
        'sele_total': sele_total,
        'less': score_request.score_sele - sele_total,
        'gpa':("%.2f"%gpa),
    }
    return render(request, 'result.html', context)

def getmajor(request):
    year = request.POST['year']
    college = request.POST['college']
    major = Major.objects.filter(year=year,college_num=college)
    major_list = {}
    for i in major:
        major_list[i.number] = i.name
    return HttpResponse(json.dumps(major_list), content_type="application/json")

def major_rebuild(request, stu_num):
    major_num = request.POST['']
    Score.objects.filter(stu_num=stu_num).update(class_num=major_num)
    MajorScore.objects.filter(stu_num=stu_num).delete()
    return HttpResponseRedirect(reverse('counter:detail', args=(stu_num,)))


#将分割成列表的成绩表以学期为单位分割
def spilt_by_term(content_list, item):
    result_list = []
    lesson_single = []
    #将内容列表中为学号的位置点全部找出
    all_point = [i for i, j in enumerate(content_list) if j == item]
    all_point.append(int(-1))
    #将列表中课程条目部分切出，
    for i in range(len(all_point)-1):
        a = all_point[i]
        b = all_point[i+1]
        result_list.append(content_list[a:b])
    for i in range(len(result_list)):
        #num_of_col用于判断每一行的栏目数
        #因为发现有部分同学某个学期的成绩表会多出一列
        #所以干脆做一个判断
        point1 = result_list[i].index('序号')
        start = result_list[i].index('备注')
        num_of_col = start-point1
        #避免成绩表格式导致索引出错
        #一般“备注”后会有一个空值，但发现有些浏览器渲染出来的内容格式有区别，其后可能出现若干个空置
        for x in range(0,10):
            if result_list[i][start+x]=='1':
                start = start + x
                break
        try:
            end = result_list[i].index('所选学分')
        except ValueError:
            end = result_list[i].index('取得学分')-2
        term = result_list[i][start:end]
        #这里将课程逐条切出
        #['序号','学期号','课程号','名称','类别（如必修）','学分','取得学分','成绩(ABCD)',
        # '绩点','学分绩点','备注（一般为空）']
        for i in range((len(term)+1)//num_of_col):
            a = term[i*num_of_col:(i+1)*num_of_col]
            if num_of_col==12:
                del a[4]
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
