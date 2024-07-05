# 为 templates（前台/用户页面）中的每个页面创建一个 URL 映射

from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/new', views.job_create, name='job_create'),
    path('job_view/<int:pk>/', views.job_view, name='job_view'),
    path('delete_job/<int:job_id>/', views.delete_job, name='job_delete'),
]