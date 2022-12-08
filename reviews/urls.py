from django.urls import path
from . import views

urlpatterns = [
    path('new/<int:product_id>/<int:user_id>/', views.create_review), 
    path('list/<int:product_id>/', views.get_review_list), 
]
