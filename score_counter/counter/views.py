from django.shortcuts import render
from django.shortcuts import render

from .models import Major, Detail

# Create your views here.
def index(request):
    result_list = Detail.objects.get_with_value('class_num', 2014172000)
    context = {
        'result_list': result_list
    }
    return render(request, 'index.html', context)