from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),   # Your core app URLs
    path('django-admin/', admin.site.urls),  # Rename to avoid conflict
]