from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^123$', views.index, name='index'),
]