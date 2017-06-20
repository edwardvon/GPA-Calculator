# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render

from .models import Major, Detail

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

def submit(request):
    range1 = {1:'公共必修课程',2:'专业核心课程',3:'专业选修课程'}
    gpa_content = request.POST['content']
    gpa_content = gpa_content.replace(' ', '\t')
    gpa_content = gpa_content.split('\t')
    a = gpa_content.index('学号')
    stu_number = gpa_content[a+1]
    # a = gpa_content.index('主修专业')
    stu_name = gpa_content[a+3]
    stu_class_name = gpa_content[a+7]
    result_list = Major.objects.get_with_value('name',stu_class_name,'year',stu_number[0:4])
    lesson_list = Detail.objects.get_with_value('class_num', int(result_list[0].number))
    context = {
        'lesson_list': lesson_list,
        'range': range1,
        'name': stu_name,
    }
    return render(request, 'index.html', context)