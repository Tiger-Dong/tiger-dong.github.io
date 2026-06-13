from django.urls import path
from . import views

urlpatterns = [
    path('new', views.index, name='index'),
    path('success/', views.success, name='success'),
]