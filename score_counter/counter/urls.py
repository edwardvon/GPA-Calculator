from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^123{1,9}$', views.index, name='index'),
]