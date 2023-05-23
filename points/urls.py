from django.urls import path, include
from . import views
from rest_framework import routers
from .views import PointHistoryViewSet

router = routers.DefaultRouter()
router.register(r'points', PointHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('history/<int:id>', views.get_point_history),
]
