from django.contrib import admin
from .models import Category, Task, SubTask

# Register your models here.
# admin.site.register(Category)
# admin.site.register(Task)
# admin.site.register(SubTask)

# Inline форма для подзадач внутри задачи
class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1 # количество пустых форм по умолчанию

@admin.register(Category)  # регистрирует класс с кастомными настройками
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Отображает категории в виде списка
    search_fields = ('name',) # Позволяет искать категории по имени

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'deadline', 'created_at') # определяет, какие поля будут видны в таблице админки
    list_filter = ('status', 'deadline') # добавляет фильтры по статусу и дедлайну, упрощая навигацию
    search_fields = ('title', 'description')  # позволяет искать задачи по title и description
    ordering = ['-created_at']  # сортирует список по убыванию даты создания.
    inlines = [SubTaskInline]

    # Укороченное отображение длинных названий
    @admin.display(description='Заголовок')
    def short_title(self, obj):
        return obj.title if len(obj.title) <= 10 else obj.title[:10] + '...'

# Action для массового изменения статуса подзадач
@admin.action(description="Пометить как 'Done'")
def mark_as_done(modeladmin, request, queryset):
    updated = queryset.update(status='done')
    modeladmin.message_user(request, f"{updated} подзадач помечено как 'Done'.")

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'description')
    ordering = ['-created_at']
    actions = [mark_as_done]