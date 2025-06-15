# projects/urls.py

from django.urls import path, include
from rest_framework_nested import routers
from .views import ProjectViewSet, TaskViewSet

# Parent router for projects
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

# Nested router for tasks under projects
projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'tasks', TaskViewSet, basename='project-tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
]
