from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

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
        unique_together = ('title', 'deadline')
        verbose_name='Задача'
        verbose_name_plural='Задачи'

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
        verbose_name='Подзадача'
        verbose_name_plural='Подзадачи'

    def __str__(self):
        return self.title
