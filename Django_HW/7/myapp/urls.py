from django.urls import path
from .views import (
    hello,
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    TaskStatsView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)

urlpatterns = [
    path('hello/', hello, name='hello'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'), # Создать задачу
    path('tasks/', TaskListView.as_view(), name='task-list'), # Список задач
    path('tasks/<int:id>/', TaskDetailView.as_view(), name='task-detail'), # Получить задачу по ID
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),  # Статистика задач
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:id>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail'),
]