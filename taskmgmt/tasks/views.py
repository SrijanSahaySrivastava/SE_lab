from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import NotFound, ValidationError
from .models import Task
from .serializers import TaskSerializer, TaskTitleSerializer
import json

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        self.after_task_created(serializer.instance)
        
    def after_task_created(self, task):
        # Add your custom processing here.
        print("Task created with ID:", task.id)
        print("Task details:", task.title, task.description, task.deadline, task.status, task.assigned_to, task.group, task.progress, task.created_at)

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)


# Endpoint to list all tasks and allow creation of a new task.
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# Endpoint to list only the titles of tasks.
class TaskTitleListView(generics.ListAPIView):
    # Changed serializer_class to TaskSerializer to include all task details.
    serializer_class = TaskSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        try:
            raw_body = request.body.decode('utf-8')
            print("TaskTitleListView raw body:", raw_body)
            self.json_data = json.loads(raw_body) if raw_body else {}
        except Exception as e:
            print("Error parsing JSON in TaskTitleListView:", e)
            self.json_data = {}

    def get_queryset(self):
        data = getattr(self, 'json_data', {}) or {}
        title = data.get('title')
        if title:
            return Task.objects.filter(title__icontains=title)
        return Task.objects.all()

# Endpoint to list tasks assigned to a specific user.
class TaskAssignedToUserListView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        try:
            raw_body = request.body.decode('utf-8')
            print("TaskAssignedToUserListView raw body:", raw_body)
            self.json_data = json.loads(raw_body) if raw_body else {}
        except Exception as e:
            print("Error parsing JSON in TaskAssignedToUserListView:", e)
            self.json_data = {}

    def get_queryset(self):
        data = getattr(self, 'json_data', {}) or {}
        username = data.get('username')
        if username:
            return Task.objects.filter(assigned_to=username)
        return Task.objects.all()
    
# New endpoint: Retrieve, update, or delete a task by its title.

class TaskByNameBodyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_task(self, request):
        title = request.data.get('title')
        if not title:
            raise ValidationError({"title": "Title field is required in the request body."})
        try:
            return Task.objects.get(title=title, created_by=request.user)
        except Task.DoesNotExist:
            raise NotFound("Task with this title not found.")

    def put(self, request, format=None):
        task = self.get_task(request)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        task = self.get_task(request)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        task = self.get_task(request)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)