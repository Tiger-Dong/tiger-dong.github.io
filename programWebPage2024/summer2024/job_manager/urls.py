from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/new', views.job_create, name='job_create'),
    path('job_view/<int:pk>/', views.job_view, name='job_view'),
    path('delete_job/<int:job_id>/', views.delete_job, name='job_delete'),
]