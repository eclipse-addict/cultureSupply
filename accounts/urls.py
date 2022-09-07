from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('register/', views.register, name='register'),
    path('delete/', views.userDelete, name='userDelete'),
    path('update/', views.userUpdate, name='userUpdate'),
    path('password/', views.changePassword, name='changePassword'),
    
]