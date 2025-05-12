from rest_framework import serializers
from .models import Task
from django.utils import timezone
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    # Make assigned_to required and disallow empty strings.
    assigned_to = serializers.CharField(required=True, allow_blank=False)
    
    class Meta:
        model = Task
        fields = '__all__'
        # Only created_by is read-only so it can be automatically set.
        read_only_fields = ['created_by']
        
    def validate_assigned_to(self, value):
        # Check if a User exists with this username.
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Assignee username does not exist.")
        return value

    def validate_deadline(self, value):
        # Check if deadline is not in the past.
        if value < timezone.now():
            raise serializers.ValidationError("Deadline must not be in the past.")
        return value
        
    def create(self, validated_data):
        # Automatically set created_by to the authenticated user from the request token.
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
        
class TaskTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title']
