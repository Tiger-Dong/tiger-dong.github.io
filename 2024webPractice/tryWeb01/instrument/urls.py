# instrument/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_instrument, name='add_instrument'),
    # 其他 URL 模式...
]