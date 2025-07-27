from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, generics, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.utils import timezone
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
import datetime
from .models import Task, SubTask, Category
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
    CategoryCreateSerializer,
    RegistrationSerializer,
)
from .permissions import IsOwnerOrReadOnly


def hello(request):
    return HttpResponse('Hello, Yevgeniy!')

# Эндпоинт для создания задачи
# class TaskCreateView(generics.CreateAPIView):
#     queryset = Task.objects.all()
#     # serializer_class = TaskSerializer
#     serializer_class = TaskCreateSerializer

# # Получение списка задач
# class TaskListView(generics.ListAPIView):
#     # queryset = Task.objects.all()
#     # serializer_class = TaskSerializer
#
#     def get(self, request):
#         day_param = request.query_params.get('day', None)
#
#         # Карта дней недели (можно расширить — добавить сокращения и английские варианты при желании)
#         DAYS = {
#             'monday': 0,
#             'tuesday': 1,
#             'wednesday': 2,
#             'thursday': 3,
#             'friday': 4,
#             'saturday': 5,
#             'sunday': 6
#         }
#
#         if day_param:
#             day_param_normalized = day_param.lower().strip()
#             if day_param_normalized in DAYS:
#                 weekday = DAYS[day_param_normalized]
#                 # Django: Sunday=1, Monday=2, ..., Saturday=7 → добавим 2
#                 django_weekday = (weekday + 2) % 7 or 7
#                 tasks = Task.objects.filter(deadline__week_day=django_weekday)
#             else:
#                 return Response(
#                     {"error": "Некорректный день недели. Пример: ?day=вторник"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#         else:
#             tasks = Task.objects.all()
#
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)

class TaskListCreateView(generics.ListCreateAPIView):
    # queryset = Task.objects.all()
    # serializer_class = TaskSerializer

    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']  # сортировка по умолчанию

    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)
        day_param = self.request.query_params.get('day', None)

        # Мапа дней недели
        days_map = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6
        }

        if day_param:
            normalized_day = day_param.lower().strip()
            if normalized_day in days_map:
                django_weekday = (days_map[normalized_day] + 2) % 7 or 7
                queryset = queryset.filter(deadline__week_day=django_weekday)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

    # при создании объекта будет назначаться текущий пользователь
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)




# Получение задачи по ID
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    # serializer_class = TaskSerializer
    serializer_class = TaskDetailSerializer
    lookup_field = 'id'

    permission_classes = [IsAuthenticated]

# # Агрегирующий эндпоинт для статистики задач
# class TaskStatsView(APIView):
#     def get(self, request):
#         total_tasks = Task.objects.count()
#         status_counts = (
#             Task.objects.values('status')
#             .annotate(count=Count('status'))
#             .order_by('status')
#         )
#         expired = Task.objects.filter(deadline__lt=timezone.now()).count()
#
#         stats = {
#             'total_tasks': total_tasks,
#             'status_distribution': {item['status']: item['count'] for item in status_counts},
#             'expired_tasks': expired
#         }
#         return Response(stats)

class TaskStatsView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_tasks = Task.objects.count()
        status_counts = (
            Task.objects.values('status')
            .annotate(count=Count('status'))
            .order_by('status')
        )
        expired = Task.objects.filter(deadline__lt=timezone.now()).count()

        stats = {
            'total_tasks': total_tasks,
            'status_distribution': {item['status']: item['count'] for item in status_counts},
            'expired_tasks': expired
        }
        return Response(stats)

class SubTaskPagination(PageNumberPagination):
    page_size = 5

# class SubTaskListCreateView(APIView):
#     def get(self, request):
#         # subtasks = SubTask.objects.all()
#         # serializer = SubTaskSerializer(subtasks, many=True)
#         # return Response(serializer.data)
#
#         task_title = request.query_params.get('task_title', None)
#         status_param = request.query_params.get('status', None)
#
#         # Извлекаем все подзадачи
#         subtasks = SubTask.objects.all()
#
#         # Фильтрация по названию главной задачи (если передано)
#         if task_title:
#             subtasks = subtasks.filter(task__title__icontains=task_title.strip())
#
#         # Фильтрация по статусу подзадачи
#         if status_param is not None:
#             status_lower = status_param.lower()
#             if status_lower in ['true', 'false']:
#                 if status_lower == 'true':
#                     subtasks = subtasks.filter(status='done')  # Например, статус == 'done'
#                 else:
#                     subtasks = subtasks.exclude(status='done')  # Остальные считаем «не завершёнными»
#             else:
#                 return Response(
#                     {"error": "Параметр 'status' должен быть 'true' или 'false'."},
#                     status=400
#                 )
#
#         # Сортировка от самых новых к старым
#         subtasks = subtasks.order_by('-created_at')
#
#         # Пагинация
#         paginator = PageNumberPagination()
#         paginator.page_size = 5
#         page = paginator.paginate_queryset(subtasks, request)
#         serializer = SubTaskSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)
#
#
#     def post(self, request):
#             serializer = SubTaskSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class SubTaskDetailUpdateDeleteView(APIView):
#     def get_object(self, id):
#         return get_object_or_404(SubTask, id=id)
#
#     def get(self, request, id):
#         subtask = self.get_object(id)
#         serializer = SubTaskSerializer(subtask)
#         return Response(serializer.data)
#
#     def put(self, request, id):
#         subtask = self.get_object(id)
#         serializer = SubTaskSerializer(subtask, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, id):
#         subtask = self.get_object(id)
#         serializer = SubTaskSerializer(subtask, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, id):
#         subtask = self.get_object(id)
#         subtask.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Получение списка и создание подзадачи
class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all().order_by('-created_at')  # сортировка от новых к старым
    # serializer_class = SubTaskSerializer
    pagination_class = SubTaskPagination

    # permission_classes = [IsAuthenticated]
    # только владельцы могли изменять и удалять свои задачи
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)

# Получение, обновление и удаление подзадачи
class SubTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    lookup_field = 'pk'

    # только авторизованные пользователи смогут получать доступ к вашему API для категорий
    permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    # queryset = Category.objects.filter(is_deleted=False)
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    # чтение любому пользователю, но запись — только аутентифицированным
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # применяем кастомный пермишен
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        # category.is_deleted = True
        # category.save()
        category.delete()
        return Response({"message": "Категория мягко удалена."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='count-tasks')
    def count_tasks(self, request, pk=None):
        data = (
            Category.all_objects.filter(is_deleted=False)
            .annotate(task_count=Count('tasks'))
            .values('id', 'name', 'task_count')
        )
        return Response(data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Для получения всех задач текущего пользователя
class MyTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


# Для получения всех подзадач текущего пользователя
class MySubTaskListView(generics.ListAPIView):
    serializer_class = SubTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


class LogoutView(APIView):
    '''
     - Принимать refresh токен из запроса (обычно в теле POST).
     - Добавлять этот токен в blacklist (аннулируя его).
     - Возвращать подтверждение выхода.
     - При этом на клиенте нужно также удалить токены (access и refresh), например, стереть куки или очистить хранилище.
    '''
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            ### Можно также удалять связанные OutstandingToken
            # tokens = OutstandingToken.objects.filter(user=request.user)
            # for t in tokens:
            #     BlacklistedToken.objects.get_or_create(token=t)

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or token is expired."}, status=status.HTTP_400_BAD_REQUEST)
