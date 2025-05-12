# filepath: c:\Users\srija\Documents\GitHub\SE_lab\taskmgmt\accounts\urls.py
from django.urls import path
from .views import UserCreateView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user_create'),
]