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
    return render(request, 'index.html', context)

def detail(request,number):
    result_list = Detail.objects.get_with_value('class_num', int(number))
    range1 = {1:'公共必修课程',2:'专业核心课程',3:'专业选修课程'}
    context = {
        'result_list': result_list,
        'range': range1
    }
    return render(request, 'detail.html', context)