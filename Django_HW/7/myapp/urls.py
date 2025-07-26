from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    hello,
    # TaskCreateView,
    # TaskListView,
    TaskListCreateView,
    TaskDetailView,
    TaskStatsView,
    SubTaskListCreateView,
    # SubTaskDetailUpdateDeleteView,
    SubTaskRetrieveUpdateDestroyView,
    CategoryViewSet,
    MyTaskListView,
    MySubTaskListView,
)

schema_view = get_schema_view(
   openapi.Info(
      title="Task Manager API",
      default_version='v1',
      description="API для управления задачами",
      contact=openapi.Contact(email="your@email.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('hello/', hello, name='hello'),
    # path('tasks/create/', TaskCreateView.as_view(), name='task-create'), # Создать задачу
    # path('tasks/', TaskListView.as_view(), name='task-list'), # Список задач
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'), # Список задач и создание
    path('tasks/<int:id>/', TaskDetailView.as_view(), name='task-detail'), # Получить задачу по ID
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),  # Статистика задач
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    # path('subtasks/<int:id>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyView.as_view(), name='subtask-detail'), # Получение, обновление и удаление подзадачи
    path('', include(router.urls)),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('my-tasks/', MyTaskListView.as_view(), name='my-task-list'),
    path('my-subtasks/', MySubTaskListView.as_view(), name='my-subtask-list'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]