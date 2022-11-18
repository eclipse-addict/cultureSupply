from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'sneaker', views.SneakerViewSet)

urlpatterns = [
    path('sneaker/', views.sneaker_list),
    path('sneaker/<int:pk>/', views.sneaker_detail),
    path('sneaker/test', views.test_req),
] 