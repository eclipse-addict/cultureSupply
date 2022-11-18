from django.urls import path, include
from . import views

# router = DefaultRouter()
# router.register(r'sneaker', views.SneakerViewSet)

urlpatterns = [
    path('new/', views.new_release_paser),
    path('brand/', views.sneaker_data_by_brand_paser),

] 