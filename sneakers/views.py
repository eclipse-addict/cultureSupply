from django.conf import settings 
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticated

from .models import Sneaker, Image
from .forms import SneakerForm
from .serializer.sneakers import SneakerListSerializer, SneakerDetailSerializer
from django.views.decorators.http import require_POST, require_safe, require_http_methods

class SneakerViewSet(ModelViewSet):
    queryset = Sneaker.objects.all()
    serializer_class = SneakerDetailSerializer
    permission_classes_by_action = {'list':           [AllowAny],
                                    'create':         [IsAuthenticated],
                                    'update':         [IsAuthenticated],
                                    'partial_update': [IsAuthenticated],
                                    'destroys':       [IsAuthenticated],
                                    
                                    }
    
    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
        

sneaker_list = SneakerViewSet.as_view({
    'get': 'list',
    'post' : 'create',
})

sneaker_detail = SneakerViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})