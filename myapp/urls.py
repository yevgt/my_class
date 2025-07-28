from django.urls import path
from .views import (
    hello_view,
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    TaskStatisticsView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    CategoryCreateView,
    CategoryUpdateView,
)

urlpatterns = [
    path('hello/', hello_view, name='hello'),
    path('api/tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('api/tasks/', TaskListView.as_view(), name='task-list'),
    path('api/tasks/<int:id>/', TaskDetailView.as_view(), name='task-detail'),
    path('api/tasks/statistics/', TaskStatisticsView.as_view(), name='task-statistics'),
    path('api/subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('api/subtasks/<int:id>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('api/categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('api/categories/<int:id>/', CategoryUpdateView.as_view(), name='category-update'),
]