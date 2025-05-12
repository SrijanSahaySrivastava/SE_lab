# filepath: c:\Users\srija\Documents\GitHub\SE_lab\taskmgmt\accounts\views.py
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer