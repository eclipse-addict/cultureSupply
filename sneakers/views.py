from django.conf import settings 
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .models import Sneaker, Image
from .forms import SneakerForm
from .serializer.sneakers import SneakerListSerializer, SneakerDetailSerializer
from django.views.decorators.http import require_POST, require_safe, require_http_methods

class SneakerViewSet(ModelViewSet):
    queryset = Sneaker.objects.all()
    serializer_class = SneakerDetailSerializer
    
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