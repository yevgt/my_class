from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
   class Meta:
       model = Task
       fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']
       read_only_fields = ['id', 'created_at']

   def validate_title(self, value):
       if Task.objects.filter(title=value).exists():
           raise serializers.ValidationError("Task with this title already exists.")
       return value

   def validate_deadline(self, value):
       from django.utils import timezone
       if value < timezone.now():
           raise serializers.ValidationError("Deadline cannot be in the past.")
       return value