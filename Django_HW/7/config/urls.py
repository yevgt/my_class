from django.contrib import admin
from django.urls import path, include

import myapp
from myapp.views import hello

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # подключаем маршруты приложения
    path('api-auth/', include('rest_framework.urls')),
]
