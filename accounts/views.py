from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
# from .forms import CustomedUserCreateForm, CustomedUserUpdateForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework import generics

class UserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer