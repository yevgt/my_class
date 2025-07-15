from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import date
from .models import (
    Task,
    SubTask,
    Category,
)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'deadline', 'status']

    def validate_deadline(self, value):
        # Проверка, что deadline не раньше сегодняшнего дня
        if value < date.today():
            raise serializers.ValidationError("Дата дедлайна не может быть в прошлом.")
        return value


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'created_at']
        read_only_fields = ['created_at']

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)  # related_name='subtasks' в модели

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'subtasks']


class SubTaskCreateSerializer(serializers.ModelSerializer):
    # Переопределяем поле created_at как только для чтения
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'created_at', 'task']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']  # укажите нужные поля

    def validate_name(self, value):
        # Проверка уникальности названия категории. Выполняется при валидации каждого поля.
        if self.instance:
            # Если мы обновляем существующий объект
            if Category.objects.exclude(id=self.instance.id).filter(name__iexact=value).exists():
                raise ValidationError('Категория с таким названием уже существует.')
        else:
            # При создании новой категории
            if Category.objects.filter(name__iexact=value).exists():
                raise ValidationError('Категория с таким названием уже существует.')
        return value

    def create(self, validated_data):
        # Валидация уже пройдена, просто создаём
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Обновляем поля (уже прошли валидацию)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance