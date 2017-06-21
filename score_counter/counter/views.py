# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render

from .models import Major,Detail,Score

# Create your views here.
def index(request):
    result_list = []
    result_list = Major.objects.get_with_value('college','信息工程学院')
    context = {
        'result_list': result_list
    }
    return render(request, 'Page1.html', context)

def detail(request,number):
    result_list = Detail.objects.get_with_value('class_num', int(number))
    range1 = {1:'公共必修课程',2:'专业核心课程',3:'专业选修课程'}
    context = {
        'result_list': result_list,
        'range': range1
    }
    return render(request, 'detail.html', context)

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
        start = result_list[i].index('学分绩点') + 1
        try:
            end = result_list[i].index('取得学分')-2
        except ValueError:
            end = -1
        result_list[i] = result_list[i][start:end]
        result_list[i][0] = '1'
    lesson_single = []
    for term in result_list:
        for i in range((len(term)+1)//10):
            a = term[i*10:(i+1)*10]
            lesson_single.append(a)
    return lesson_single
#
def score_insert(list,stu_num,class_num):
    for item in list:
        a = item[1:]
        a.append(str(stu_num))
        a.append(str(class_num))
        Score.objects.score_init(a)
    return 1

def submit(request):
    range1 = {1:'公共必修课程',2:'专业核心课程',3:'专业选修课程'}
    gpa_content = request.POST['content']
    gpa_content = gpa_content.replace(':','\t')
    gpa_content = gpa_content.split('\t')
    try:
        index = gpa_content.index('姓名')
    except ValueError:
        return render(request, 'Page1.html', {'error_message': "噢！同学你是不是复制错了，看看说明吧"})
    stu_number = gpa_content[index-1]
    stu_class_name = gpa_content[index+5].split(' ')[0]
    major_num = Major.objects.get_with_value('name',stu_class_name,'year',stu_number[0:4])[0].number
    # lesson_list = Detail.objects.get_with_value('class_num', int(result_list[0].number))
    result_list = spilt_by_term(gpa_content, stu_number)
    score_insert(result_list,stu_number,major_num)
    fuck = Score.objects.get_all()
    context = {
        # 'lesson_list': lesson_list,
        # 'range': range1,
        'name': major_num,
        # 'a': a,
        'result':fuck,
    }
    return render(request, 'index.html', context)