from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('create/updator/',views.create_updator),
    path('updator/list/',views.get_updator_list),
]