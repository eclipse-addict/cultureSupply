from django.urls import path
from . import views

urlpatterns = [
    path('review/<int:product_id>/<int:user_id>/', views.create_review) 
]
