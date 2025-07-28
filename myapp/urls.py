from django.urls import path
from .views import (
    hello_view,
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    TaskStatisticsView,
)

urlpatterns = [
    path('hello/', hello_view, name='hello'),
    path('api/tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('api/tasks/', TaskListView.as_view(), name='task-list'),
    path('api/tasks/<int:id>/', TaskDetailView.as_view(), name='task-detail'),
    path('api/tasks/statistics/', TaskStatisticsView.as_view(), name='task-statistics'),
]