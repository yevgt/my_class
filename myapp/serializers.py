from rest_framework import serializers
from .models import Task, SubTask, Category
from django.utils import timezone


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

class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'task', 'status', 'deadline', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_title(self, value):
        if SubTask.objects.filter(title=value).exists():
            raise serializers.ValidationError("SubTask with this title already exists.")
        return value

    def validate_deadline(self, value):
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_deleted', 'deleted_at'] # чтобы они отображались в ответах, но не могли изменяться через API.
        read_only_fields = ['id', 'is_deleted', 'deleted_at']

    def create(self, validated_data):
        name = validated_data['name']
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        if name != instance.name and Category.objects.filter(name=name).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        instance.name = name
        instance.save()
        return instance

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'subtasks']
        read_only_fields = ['id', 'created_at']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_title(self, value):
        if Task.objects.filter(title=value).exists():
            raise serializers.ValidationError("Task with this title already exists.")
        return value

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value