from django.conf.urls import url
from . import views

app_name = 'counter'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<number>[0-9]+)/$', views.detail, name='detail'),
    url(r'submit/$', views.submit, name='submit'),
]