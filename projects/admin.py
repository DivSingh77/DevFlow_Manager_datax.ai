# projects/admin.py

from django.contrib import admin
from .models import Project, Task
from .models import ActionLog

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'due_date', 'project')  # ✅ Use due_date only if it's in the model
    search_fields = ('title',)
    list_filter = ('due_date', 'project')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'duration', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    
@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'ip_address', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('action', 'ip_address')
