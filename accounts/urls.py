from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.UserCreate.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('signup/', views.signup, name='signup'),
    # path('register/', views.register, name='register'),
    # path('delete/', views.userDelete, name='userDelete'),
    # path('update/', views.userUpdate, name='userUpdate'),
    # path('password/', views.changePassword, name='changePassword'),
    
]