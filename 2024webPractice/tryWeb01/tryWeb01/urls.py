# tryWeb01/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('instrument/', include("instrument.urls")),  # 确保这里正确引用了 instrument 的 urls
]