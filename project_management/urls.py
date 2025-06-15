# project_management/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from projects.views import api_root
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', api_root),  # Optional: homepage root
    path('admin/', admin.site.urls),
    path('api/', include('projects.urls')),  # All API endpoints here
    path('api/token-auth/', obtain_auth_token),  # Token-based login
    path('api-auth/', include('rest_framework.urls')),  # For browsable API login
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
