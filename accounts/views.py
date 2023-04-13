import jwt
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status, viewsets, response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from cultureSupply.settings import SECRET_KEY
from points.views import new_user_point
from django.contrib.auth import get_user_model
from allauth.account.models import EmailConfirmation, EmailAddress
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from dj_rest_auth.registration.views import ConfirmEmailView
from django.urls import reverse_lazy
from django.views.generic import View
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

User = get_user_model()



# @api_view(['POST',])
# @permission_classes([AllowAny])
# def create_userInfo(request, user_pk):
#     user = get_object_or_404(User, pk=user_pk)
    
#     if request.method == 'POST':
#         serializer = UserInfoSerializer(data=request.data)
        
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=user)
#             new_user_point(user_pk)
            
#             return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def get_update_userInfo(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    userInfo = get_object_or_404(UserInfo, user=user)

    if request.method == 'GET':
        serializer = UserInfoSerializer(userInfo)
        return JsonResponse(serializer.data, safe=False)
    
        
    elif request.method == 'PUT':
        pass


@api_view(['GET',])
@permission_classes([AllowAny])
def nick_name_check(request):
    nickCheck = UserInfo.objects.filter(nick_name=request.GET.get('nick_name'))
    
    if nickCheck:
        return HttpResponse(status=status.HTTP_226_IM_USED)
    return HttpResponse(status=status.HTTP_200_OK)



@api_view(['GET',])
@permission_classes([AllowAny])
def email_check(request):
    emailCheck = User.objects.filter(email=request.GET.get('email'))
    
    if emailCheck:
        return HttpResponse(status=status.HTTP_226_IM_USED)
    return HttpResponse(status=status.HTTP_200_OK)

# 이메일 인증 관련    
class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        print(confirmation)
        confirmation.confirm(self.request)
        
        # 이메일 인증이 성공한 시점에, 유저정보 테이블을 생성한다. 
        info_table_created = self.create_userInfo()
        if info_table_created:
            return HttpResponseRedirect('https://www.kickin.kr/')
        # 이메일 인증이 성공한 뒤, 이메일 인증이 성공했다는 화면으로 이동. 
        return HttpResponseRedirect('https://www.kickin.kr/404/')
    def create_userInfo(self):
        key = self.kwargs['key']
        user = EmailConfirmationHMAC.from_key(key).email_address.user
        userInfo = UserInfo.save(user=user, first_name=user.first_name, last_name=user.last_name, nick_name=user.nick_name)
        new_user_point(user.pk)
        
        if userInfo: 
            return True
        
        return False


    def get_object(self, queryset=None):
        key = self.kwargs['key']
        print('key: ', key)
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        print('email_confirmation: ', email_confirmation)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                return HttpResponseRedirect('/login/failure/')
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs
    
    

@method_decorator(csrf_exempt, name='dispatch')
class ResendConfirmationView(View):
    # success_url = reverse_lazy('account_email_verification_sent')
    email_template_name = 'registration/verification_email.html'
    # subject_template_name = 'registration/verification_email_subject.txt'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        user_email = EmailAddress.objects.get(email=email)
        verification_key = EmailAddress.objects.get(email=email)
        
        print('email : ',request.POST.get('email'))
        print('user : ', user)
        print('verification_key : ', verification_key)
        if user_email.verified:
            print('user.is_active : ', user.is_active)
            data = {
                'message': '이미 이메일 주소 인증이 확인되었습니다.'
            }
            return HttpResponse(content=data, status=status.HTTP_200_OK)

        key = EmailConfirmationHMAC(user.emailaddress_set.get(email=user.email)).key
        print()
        context = {
            'user': user,
            # /user/dj-rest-auth/registration/account-confirm-email/
            'activate_url': request.build_absolute_uri(reverse_lazy('account_confirm_email', kwargs={'key': key})),
        }
        message = render_to_string(self.email_template_name, context)
        send_mail(
            subject='[Kickin] 이메일 주소 확인',
            message='',
            html_message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        data = {
            'msg': '확인 이메일이 이메일 주소로 전송되었습니다.',
            'status_code': '200'
            }
        return JsonResponse(data=data, status=status.HTTP_200_OK)






