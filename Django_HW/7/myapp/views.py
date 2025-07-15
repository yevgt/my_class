from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Count, Q
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
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

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
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data)

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

