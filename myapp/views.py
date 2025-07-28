from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task, SubTask, Category
from .serializers import (
    TaskSerializer,
    SubTaskCreateSerializer,
    CategoryCreateSerializer,
    TaskDetailSerializer,
    TaskCreateSerializer,
)

def hello_view(request):
    return HttpResponse("<h1>Hello, YevgeniyG</h1>")

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

    def perform_create(self, serializer):
        serializer.save()

# Возвращает список всех задач через GET-запрос.
class TaskListView(generics.ListAPIView):
    # queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        day_of_week = self.request.query_params.get('day_of_week', None)
        if day_of_week:
            # Преобразуем день недели в число (1=понедельник, 7=воскресенье)
            day_map = {
                'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4,
                'friday': 5, 'saturday': 6, 'sunday': 7
            }
            day_number = day_map.get(day_of_week.lower())
            if day_number:
                # Фильтруем по дню недели
                queryset = queryset.annotate(week_day=ExtractWeekDay('deadline_date')).filter(week_day=day_number)
            else:
                # Если день недели некорректен, возвращаем пустой queryset
                queryset = queryset.none()
        return queryset

# Возвращает задачу по id через GET-запрос.
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_field = 'id'

# Агрегирующий эндпоинт для статистики задач
class TaskStatisticsView(APIView):
    def get(self, request):
        total_tasks = Task.objects.count()
        status_counts = Task.objects.values('status').annotate(count=Count('status'))
        overdue_tasks = Task.objects.filter(deadline__lt=timezone.now()).count()

        stats = {
            'total_tasks': total_tasks,
            'status_counts': {item['status']: item['count'] for item in status_counts},
            'overdue_tasks': overdue_tasks
        }
        return Response(stats)


class SubTaskListCreateView(generics.ListCreateAPIView):
    # queryset = SubTask.objects.all().order_by('-created_at') # сортировка по убыванию
    serializer_class = SubTaskCreateSerializer

    def get_queryset(self):
        queryset = SubTask.objects.all().order_by('-created_at')
        task_title = self.request.query_params.get('task_title', None)
        status = self.request.query_params.get('status', None)
        if task_title:
            queryset = queryset.filter(task__title=task_title)
        if status:
            queryset = queryset.filter(status=status.upper())
        return queryset

    def perform_create(self, serializer):
        serializer.save()


class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    lookup_field = 'id'


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    def perform_create(self, serializer):
        serializer.save()


# class CategoryUpdateView(generics.UpdateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryCreateSerializer
#     lookup_field = 'id'

class CategoryDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    lookup_field = 'id'