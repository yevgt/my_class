from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import Count, Q
import datetime
from .models import Task, SubTask
from .serializers import (
    TaskSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    TaskCreateSerializer,
)

def hello(request):
    return HttpResponse('Hello, Yevgeniy!')

# Эндпоинт для создания задачи
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    # serializer_class = TaskSerializer
    serializer_class = TaskCreateSerializer

# Получение списка задач
class TaskListView(generics.ListAPIView):
    # queryset = Task.objects.all()
    # serializer_class = TaskSerializer

    def get(self, request):
        day_param = request.query_params.get('day', None)

        # Карта дней недели (можно расширить — добавить сокращения и английские варианты при желании)
        DAYS = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6
        }

        if day_param:
            day_param_normalized = day_param.lower().strip()
            if day_param_normalized in DAYS:
                weekday = DAYS[day_param_normalized]
                # Django: Sunday=1, Monday=2, ..., Saturday=7 → добавим 2
                django_weekday = (weekday + 2) % 7 or 7
                tasks = Task.objects.filter(deadline__week_day=django_weekday)
            else:
                return Response(
                    {"error": "Некорректный день недели. Пример: ?day=вторник"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            tasks = Task.objects.all()

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)



# Получение задачи по ID
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    # serializer_class = TaskSerializer
    serializer_class = TaskDetailSerializer
    lookup_field = 'id'

# Агрегирующий эндпоинт для статистики задач
class TaskStatsView(APIView):
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

class SubTaskListCreateView(APIView):
    def get(self, request):
        # subtasks = SubTask.objects.all()
        # serializer = SubTaskSerializer(subtasks, many=True)
        # return Response(serializer.data)

        task_title = request.query_params.get('task_title', None)
        status_param = request.query_params.get('status', None)

        # Извлекаем все подзадачи
        subtasks = SubTask.objects.all()

        # Фильтрация по названию главной задачи (если передано)
        if task_title:
            subtasks = subtasks.filter(task__title__icontains=task_title.strip())

        # Фильтрация по статусу подзадачи
        if status_param is not None:
            status_lower = status_param.lower()
            if status_lower in ['true', 'false']:
                if status_lower == 'true':
                    subtasks = subtasks.filter(status='done')  # Например, статус == 'done'
                else:
                    subtasks = subtasks.exclude(status='done')  # Остальные считаем «не завершёнными»
            else:
                return Response(
                    {"error": "Параметр 'status' должен быть 'true' или 'false'."},
                    status=400
                )

        # Сортировка от самых новых к старым
        subtasks = subtasks.order_by('-created_at')

        # Пагинация
        paginator = PageNumberPagination()
        paginator.page_size = 5
        page = paginator.paginate_queryset(subtasks, request)
        serializer = SubTaskSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


    def post(self, request):
            serializer = SubTaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, id):
        return get_object_or_404(SubTask, id=id)

    def get(self, request, id):
        subtask = self.get_object(id)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, id):
        subtask = self.get_object(id)
        serializer = SubTaskSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        subtask = self.get_object(id)
        serializer = SubTaskSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        subtask = self.get_object(id)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

