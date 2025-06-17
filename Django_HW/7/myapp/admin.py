from django.contrib import admin
from .models import Category, Task, SubTask

# Register your models here.
# admin.site.register(Category)
# admin.site.register(Task)
# admin.site.register(SubTask)

@admin.register(Category)  # регистрирует класс с кастомными настройками
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Отображает категории в виде списка
    search_fields = ('name',) # Позволяет искать категории по имени

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at') # определяет, какие поля будут видны в таблице админки
    list_filter = ('status', 'deadline') # добавляет фильтры по статусу и дедлайну, упрощая навигацию
    search_fields = ('title', 'description')  # позволяет искать задачи по title и description
    ordering = ['-created_at']  # сортирует список по убыванию даты создания.

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'description')
    ordering = ['-created_at']