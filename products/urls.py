from django.urls import path, include
from . import views

urlpatterns = [
    path('img/main/', views.main_img),
    path('sneaker/', views.get_sneaker),
    path('sneaker/<int:id>/', views.get_detail),
    
    # urls for admin
    path('new/', views.new_release_paser),
    path('brand/', views.sneaker_data_by_brand_paser),
    path('test/', views.google_img_download),
    path('popular/', views.popular_release),
    path('img/pasing/', views.sneaker_img_paser),
    path('goat/', views.get_goat),
    path('goat/pop/', views.goat_popular_release_recent_kicks),
    path('dup/', views.duplicate_check)
    
    

] 