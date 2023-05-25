from django.urls import path
from . import views
from .views import RaffleViewSet, RaffleEntryViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', RaffleViewSet)
router.register(r'raffleEntry', RaffleEntryViewSet)
urlpatterns = router.urls
