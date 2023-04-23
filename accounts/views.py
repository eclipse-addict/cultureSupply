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
        returned_mail = None

        if type(confirmation) != HttpResponseRedirect:
            returned_mail = confirmation.confirm(self.request)

        if returned_mail:
            return HttpResponseRedirect('https://www.kickin.kr/')

        return HttpResponseRedirect('https://www.kickin.kr/404/')


    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
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


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def get_update_create_userinfo(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user_info, created = UserInfo.objects.get_or_create(user=user)

    if request.method == 'GET':
        serializer = UserInfoSerializer(user_info)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        print(request.data)
        serializer = UserInfoSerializer(user_info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)

