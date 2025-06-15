from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
import csv

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

# Filtering for Project model
class ProjectFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    start_date = filters.DateFromToRangeFilter()
    end_date = filters.DateFromToRangeFilter()

    class Meta:
        model = Project
        fields = ['name', 'start_date', 'end_date']

# Project ViewSet
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_active=True).order_by('-id')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProjectFilter

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['POST'])
    def image(self, request, pk=None):
        project = self.get_object()
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        project.image = request.FILES['image']
        project.save()
        return Response(ProjectSerializer(project, context={'request': request}).data)

    @action(detail=False, methods=['GET'])
    def export(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="projects.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Description', 'Start Date', 'End Date', 'Duration'])
        
        for project in Project.objects.filter(is_active=True):
            writer.writerow([
                project.name,
                project.description,
                project.start_date,
                project.end_date,
                project.duration
            ])
        
        return response

    @action(detail=True, methods=['GET'])
    def download_csv(self, request, pk=None):
        project = self.get_object()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{project.name}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Project Name', 'Description', 'Start Date', 'End Date', 'Duration'])
        writer.writerow([
            project.name,
            project.description,
            project.start_date,
            project.end_date,
            project.duration
        ])

        return response

# Task ViewSet
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs['project_pk'])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(project=project)

# Root API View
@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        "message": "Welcome to the Project Management API",
        "endpoints": {
            "projects": "/api/projects/",
            "nested_tasks": "/api/projects/<project_id>/tasks/"
        }
    })
