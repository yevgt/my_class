from django.contrib import admin
from .models import Category, Task, SubTask

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1  # Количество пустых форм по умолчанию
    fields = ('title', 'description', 'status', 'deadline')
    show_change_link = True  # Ссылка для редактирования подзадачи

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'deadline_date', 'created_at', 'get_categories')
    list_filter = ('status', 'deadline', 'categories')
    search_fields = ('title', 'description')
    date_hierarchy = 'deadline'
    filter_horizontal = ('categories',)
    ordering = ('-created_at',)
    list_per_page = 25
    inlines = [SubTaskInline]  # Добавляем инлайн-форму для подзадач

    # укороченное отображение в списке подзадач
    def short_title(self, obj):
        return obj.title[:10] + '...' if len(obj.title) > 10 else obj.title

    short_title.short_description = 'Title'

    def get_categories(self, obj):
        return ", ".join(category.name for category in obj.categories.all())
    get_categories.short_description = 'Categories'

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline', 'task')
    search_fields = ('title', 'description')
    date_hierarchy = 'deadline'
    ordering = ('-created_at',)
    list_per_page = 25

    # создание акшена
    actions = ['make_done']

    def make_done(self, request, queryset):
        updated = queryset.update(status='DONE')
        self.message_user(request, f"{updated} subtask(s) marked as Done.")

    make_done.short_description = "Mark selected subtasks as Done"