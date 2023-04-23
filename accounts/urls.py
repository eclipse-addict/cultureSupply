from django.urls import path, include, re_path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.registration.views import (
    VerifyEmailView, RegisterView
)
from .views import ConfirmEmailView, ResendConfirmationView 


urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),

    # 이메일 관련 필요
    path('accounts/allauth/', include('allauth.urls')),

    # 유효한 이메일이 유저에게 전달
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('resend-confirmation/', ResendConfirmationView.as_view(), name='resend_confirmation'),

    path('rest-auth/registration/', RegisterView.as_view(), name='rest_register'),
    re_path(r'^dj-rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('nickcheck/', views.nick_name_check),
    path('emailcheck/', views.email_check),

    # UserInfo related urls
    path('userinfo/<int:user_pk>/', views.get_update_create_userinfo),
]





