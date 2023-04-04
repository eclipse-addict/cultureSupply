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

@api_view(['POST',])
@permission_classes([AllowAny])
def create_userInfo(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    
    if request.method == 'POST':
        serializer = UserInfoSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            new_user_point(user_pk)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)



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

    
class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        print(confirmation)
        confirmation.confirm(self.request)
        return HttpResponseRedirect('/login/success/')

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