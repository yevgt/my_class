from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")

    class Meta:
        db_table = 'task_manager_category'  # Имя таблицы в базе данных
        verbose_name = "Категория"     # "Category" Человекочитаемое имя модели
        verbose_name_plural = "Категории"  # "Categories"  Человекочитаемое множественное число имени модели
        unique_together = ('name',)  # Уникальность по полю name

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]
    title = models.CharField(max_length=255, unique=True, verbose_name="Название задачи")
    description = models.TextField(blank=True, null=True, verbose_name="Описание задачи")
    categories = models.ManyToManyField(Category, related_name="tasks", verbose_name="Категории задачи")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус задачи")
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        unique_together = ('title',) # 'deadline') # Уникальность по полю title
        verbose_name='Задача'  # 'Task' Человекочитаемое имя модели
        verbose_name_plural='Задачи' # 'Tasks'  Человекочитаемое множественное число имени модели
        db_table = 'task_manager_task' # Имя таблицы в базе данных
        ordering = ['-created_at']  # Сортировка по убыванию даты создания

    def __str__(self):
        return self.title

class SubTask(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Название подзадачи")
    description = models.TextField(blank=True, null=True, verbose_name="Описание подзадачи")
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE, verbose_name="Основная задача")
    status = models.CharField(max_length=20, choices=Task.STATUS_CHOICES, default='new', verbose_name="Статус подзадачи")
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        db_table = 'task_manager_subtask'  # Имя таблицы в базе данных
        ordering = ['-created_at']  # Сортировка по убыванию даты создания
        verbose_name='Подзадача' # 'SubTask' Человекочитаемое имя модели
        verbose_name_plural='Подзадачи'  # 'SubTasks'  Человекочитаемое множественное число имени модели
        unique_together = ('title',)  # Уникальность по полю title

    def __str__(self):
        return self.title
