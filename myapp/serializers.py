from rest_framework import serializers
from .models import Task, SubTask, Category
from django.utils import timezone
from django.contrib.auth.models import User
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        if not value.strip():
            raise serializers.ValidationError("Username cannot be empty.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_password(self, value):
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at','owner']

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
        fields = ['id', 'title', 'description', 'task', 'status', 'deadline', 'created_at', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']

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
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'subtasks', 'owner']
        read_only_fields = ['id', 'created_at', 'owner']

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