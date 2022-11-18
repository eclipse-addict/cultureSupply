from django.urls import path, include
from . import views

# router = DefaultRouter()
# router.register(r'sneaker', views.SneakerViewSet)

urlpatterns = [
    path('search/<str:query>', views.stockX_data_paser),

] 