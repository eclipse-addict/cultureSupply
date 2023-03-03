from django.urls import path, include
from . import views
from .views import ProductListViewSet
urlpatterns = [
    path('img/main/', views.main_img),
    # path('sneaker/', views.get_sneaker),
    path('sneaker/<int:id>/', views.get_detail),
    path('sneaker/like/<int:product_id>/<int:user_id>/', views.product_like),
    path('sneaker/list/', ProductListViewSet.as_view()),
    
    # urls for admin
    path('new/', views.new_release_paser),
    path('brand/', views.sneaker_data_by_brand_paser),
    path('test/', views.google_img_download),
    path('popular/', views.popular_release),
    path('img/pasing/', views.sneaker_img_paser), # 이미지 다운로더 
    path('goat/', views.get_goat),
    path('goat/collections/', views.goat_collections),
    path('dup/', views.duplicate_check),
    path('imgmodel/', views.temp_img_fix),
    
    path('imgmodeladd/', views.select_all_and_add_img_model),
    
    # path('imgupdator/', views.img_url_updator), # 이미지 Url Localhost -> https://www.kickin.co.kr/ 로 변경
    
    
    
    

] 