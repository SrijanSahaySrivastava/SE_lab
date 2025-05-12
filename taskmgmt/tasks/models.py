
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, default='Pending')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.CharField(max_length=128)
    group = models.CharField(max_length=128, blank=True)
    progress = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
