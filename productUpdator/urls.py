from . import views
from django.urls import path, include
from rest_framework import routers
from .views import UpdatorViewSet

router = routers.DefaultRouter()
router.register(r'updators', UpdatorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/updator/', views.create_updator),
    path('accpet/<int:pk>/', views.accept_updator),
    path('deny/<int:pk>/', views.deny_updator),

]