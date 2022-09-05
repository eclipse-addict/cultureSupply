from django.urls import path
from . import views

app_name = 'sneakers'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/', views.detail, name='detail'),
    
]