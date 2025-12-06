# Django
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter



# router = DefaultRouter()
# router.register(r'main', AuthorizationView, basename='Authorization')

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('reg/', include('user.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    
]
