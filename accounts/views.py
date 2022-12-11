import jwt
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.http import HttpResponse, JsonResponse
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status, viewsets, response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from cultureSupply.settings import SECRET_KEY



@api_view(['GET', 'POST', 'PUT',])
def userInfo(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    userInfo = get_object_or_404(UserInfo, user=user)
    if request.method == 'GET':
        serializer = UserInfoSerializer(userInfo)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        print(f'request.POST: {request.POST}')
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # print(f'serializers: {serializers.data}')
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
