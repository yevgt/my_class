from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Task(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In progress'),
        ('PENDING', 'Pending'),
        ('BLOCKED', 'Blocked'),
        ('DONE', 'Done'),
    )

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    deadline = models.DateTimeField()
    deadline_date = models.DateField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.deadline.date()})"

    def save(self, *args, **kwargs):
        # Автоматически устанавливаем deadline_date из deadline
        self.deadline_date = self.deadline.date()
        super().save(*args, **kwargs)

    def clean(self):
        # Дополнительная валидация
        if not self.title.strip():
            raise ValidationError("Title cannot be empty.")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'deadline_date'],
                name='unique_title_per_date'
            )
        ]
        db_table = 'task_manager_task'
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-created_at']

class SubTask(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In progress'),
        ('PENDING', 'Pending'),
        ('BLOCKED', 'Blocked'),
        ('DONE', 'Done'),
    )

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Subtask of {self.task.title})"

    def clean(self):
        # Дополнительная валидация
        if not self.title.strip():
            raise ValidationError("Title cannot be empty.")

    class Meta:
        db_table = 'task_manager_subtask'
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
        ordering = ['-created_at']