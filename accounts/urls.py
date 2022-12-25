from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    
    path('userinfo/<int:user_pk>/', views.create_userInfo),
    path('userinfo/get/<int:user_pk>/', views.get_update_userInfo),
    path('nickcheck/', views.nick_name_check),
    path('emailcheck/', views.email_check),
]
    
