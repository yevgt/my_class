from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import date
from django.contrib.auth import get_user_model
from .models import (
    Task,
    SubTask,
    Category,
)
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator

User = get_user_model()

# Сериализатор для создания/обновления категории с проверкой уникальности
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

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
        instance.name = validated_data.get('name', instance.name) # обновляем имя категории
        instance.description = validated_data.get('description', instance.description)  # Обновляем описание
        instance.save()
        return instance

# Сериализатор для вывода задач
class TaskSerializer(serializers.ModelSerializer):
    categories = CategoryCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
              'id',
              'title',
              'categories',
              'description',
              'status',
              'deadline',
              'created_at',
              'owner',
        ]
        read_only_fields = ['owner', 'created_at']

        def update(self, instance, validated_data):
            # Если deadline не передан — сохранить текущее значение из instance
            if 'deadline' not in validated_data or validated_data['deadline'] is None:
                validated_data['deadline'] = instance.deadline

            return super().update(instance, validated_data)

# Сериализатор для создания/обновления задачи с валидацией
class TaskCreateSerializer(serializers.ModelSerializer):
    # выводим имя категории
    categories = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'categories',
            'deadline',
            'status',
            'owner',
        ]

    def validate_deadline(self, value):
        # Проверка, что deadline не раньше сегодняшнего дня
        if value.date() < date.today():
            raise serializers.ValidationError("Дата дедлайна не может быть в прошлом.")
        return value

# Сериализатор детальной задачи с вложенными подзадачами
class TaskDetailSerializer(serializers.ModelSerializer):
    # subtasks = SubTaskSerializer(many=True, read_only=True)  # related_name='subtasks' в модели
    subtasks = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id',
                  'title',
                  'description',
                  'status',
                  'deadline',
                  'created_at',
                  'subtasks'
        ]

    def get_subtasks(self, obj):
        subtasks = obj.subtasks.all().order_by('-created_at')  # предполагается related_name='subtasks'
        return SubTaskSerializer(subtasks, many=True).data

# Сериализатор для вывода подзадач с фильтрацией/поиском
class SubTaskSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = ['id',
                  'title',
                  'description',
                  'status',
                  'deadline',
                  'task',
                  'task_title',
                  'created_at',
                  'owner',
        ]
        read_only_fields = ['owner', 'created_at']

# Сериализатор для создания/обновления подзадачи
class SubTaskCreateSerializer(serializers.ModelSerializer):
    # Переопределяем поле created_at как только для чтения
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = ['id',
                  'title',
                  'description',
                  'status',
                  'deadline',
                  'task',
                  'created_at',
        ]
        read_only_fields = ['created_at']

# Сериализатор регистрации
class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Повтор пароля")
    username = serializers.CharField(
        required=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Допустимы буквы, цифры и @/./+/-/_ символы.'
        )]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        # Пароли совпадают
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Пароли не совпадают."})

        # Уникальность email
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email': "Пользователь с таким email уже существует."})

        # Уникальность username
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({'username': "Пользователь с таким username уже существует."})

        return attrs

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user