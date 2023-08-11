from django.urls import path
from . import views
from .views import ApiProductListViewSet

from rest_framework import routers

router = routers.DefaultRouter()

# 서로 다른 path 함수를 하나로 묶어 주는 과정
# url prefix, ViewSet
router.register(r'product', ApiProductListViewSet, basename='product')

urlpatterns = router.urls

urlpatterns += [
    path('register/', views.api_register)
]
