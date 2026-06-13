from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('instrument.urls')),  # 调整为你的应用的urls
]