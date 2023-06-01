from django.urls import path
from . import views
from .views import RaffleViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', RaffleViewSet)

urlpatterns = [
    path('entries/', views.raffle_entry),
]

urlpatterns += router.urls
