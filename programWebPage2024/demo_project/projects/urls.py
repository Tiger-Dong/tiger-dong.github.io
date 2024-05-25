from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/new', views.project_create, name='project_create'),
    path('edit_project/<int:pk>/', views.edit_project, name='edit_project'),
]