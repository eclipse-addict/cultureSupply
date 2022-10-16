from django.urls import path
from . import views

app_name = 'sneakers'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/', views.detail, name='detail'),
    
    path('v1/index', views.v1_index, name='v1_index'),
    path('v1/create/', views.v1_create, name='v1_create'),
    
]