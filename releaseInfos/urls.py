from django.urls import path, include, re_path
from . import views
from django.conf import settings

urlpatterns = [
    path('sneaker/<prd_sku>/', views.get_ongoing_release_detail),
    path('prices/<prd_sku>/', views.get_kream_price_Info),
    path('sku/<prd_sku>/', views.sku_search),

]