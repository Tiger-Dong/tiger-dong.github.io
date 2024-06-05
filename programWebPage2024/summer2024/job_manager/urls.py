from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('job/new', views.job_create, name='job_create'),
    path('edit_job/<int:pk>/', views.edit_job, name='edit_job'),
    path('job_view/<int:pk>/', views.job_view, name='job_view'),
]