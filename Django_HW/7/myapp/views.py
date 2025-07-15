from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Count, Q
from .models import Task
from .serializers import TaskSerializer

# Эндпоинт для создания задачи
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# Получение списка задач
class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# Получение задачи по ID
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
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

def hello(request):
    return HttpResponse('Hello, Yevgeniy!')
