from rest_framework import serializers
from .models import Project, Task

class TaskSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(source='project.id', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'project', 'project_name', 'title', 'description', 
                 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date',
                 'duration', 'image', 'image_url', 'is_active', 'tasks',
                 'created_at', 'updated_at']
        read_only_fields = ['duration', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None