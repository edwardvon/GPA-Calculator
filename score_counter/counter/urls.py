from django.conf.urls import url
from . import views

app_name = 'counter'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<stu_num>[0-9]+)/$', views.detail, name='detail'),
    url(r'submit/$', views.submit, name='submit'),
    url(r'^(?P<stu_num>[0-9]+)/result/$', views.result, name='result'),
    url(r'^getmajor/$',views.getmajor, name='getmajor'),
    url(r'^(?P<stu_num>[0-9]+)/rebuilt/$', views.major_rebuild, name='major_rebuild'),
]