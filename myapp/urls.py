from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
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
    CurrentUserTasksView,
    UserRegistrationView,
    CustomTokenObtainPairView,
    LogoutView,
)
from rest_framework.routers import DefaultRouter

schema_view = get_schema_view(
       openapi.Info(
           title="Task Manager API",
           default_version='v1',
           description="API for managing tasks, subtasks, and categories",
           terms_of_service="https://www.example.com/terms/",
           contact=openapi.Contact(email="contact@example.com"),
           license=openapi.License(name="MIT License"),
       ),
       public=True,
)

router = DefaultRouter() # для автоматической генерации маршрутов
router.register(r'categories', CategoryViewSet, basename='category')
urlpatterns = [
    path('hello/', hello_view, name='hello'),
    # path('api/tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('api/tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('api/tasks/<int:id>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail-update-delete'),
    path('api/tasks/my/', CurrentUserTasksView.as_view(), name='current-user-tasks'),
    path('api/tasks/statistics/', TaskStatisticsView.as_view(), name='task-statistics'),
    path('api/subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('api/subtasks/<int:id>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    # path('api/categories/create/', CategoryCreateView.as_view(), name='category-create'),
    # path('api/categories/<int:id>/', CategoryDetailUpdateView.as_view(), name='category-update'),
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]