from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TaskListCreateView, TaskTitleListView, TaskAssignedToUserListView, TaskByNameBodyView
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('tasks/titles/', TaskTitleListView.as_view(), name='task-title-list'),
    path('tasks/user/', TaskAssignedToUserListView.as_view(), name='task-assigned-to-user-list'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/create/', TaskViewSet.as_view({'post': 'create'}), name='task-create'),
    path('tasks/byname/', TaskByNameBodyView.as_view(), name='task-by-name-body'),
    path('', include(router.urls)),
]