from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.IntegerField()
    image = models.ImageField(upload_to='projects/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.duration = (self.end_date - self.start_date).days
        super().save(*args, **kwargs)

class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('TODO', 'To Do'),
            ('IN_PROGRESS', 'In Progress'),
            ('DONE', 'Done')
        ],
        default='TODO'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class UserAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"

class ActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} did '{self.action}' at {self.timestamp}"
