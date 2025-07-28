from django.urls import path, include
from .views import (
    hello_view,
    # TaskCreateView,
    # TaskListView,
    # TaskDetailView,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TaskStatisticsView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    # CategoryCreateView,
    # CategoryUpdateView,
    # CategoryDetailUpdateView,
    CategoryViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter() # для автоматической генерации маршрутов
router.register(r'categories', CategoryViewSet, basename='category')
urlpatterns = [
    path('hello/', hello_view, name='hello'),
    # path('api/tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('api/tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('api/tasks/<int:id>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail-update-delete'),
    path('api/tasks/statistics/', TaskStatisticsView.as_view(), name='task-statistics'),
    path('api/subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('api/subtasks/<int:id>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    # path('api/categories/create/', CategoryCreateView.as_view(), name='category-create'),
    # path('api/categories/<int:id>/', CategoryDetailUpdateView.as_view(), name='category-update'),
    path('api/', include(router.urls)),
]