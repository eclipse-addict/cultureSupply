from rest_framework.decorators import api_view, permission_classes
import random
import string
from pprint import pprint as pp

import requests
from allauth.account.models import EmailAddress
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from points.views import new_user_point
from .serializers import *

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def kakao_login_and_get_userinfo(request):
    code = request.data.get('code')
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
    }
    body = {
        'grant_type': 'authorization_code',
        'client_id': 'dcf8cc38ec4e7ec39baf6207a53ed140',
        'redirect_uri': 'http://localhost:8080/loading/',
        'code': code,
    }
    response = requests.post(headers=headers, url='https://kauth.kakao.com/oauth/token', data=body)
    access_token = response.json().get('access_token')

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    }

    info_request = requests.get(url='https://kapi.kakao.com/v2/user/me', headers=headers)
    info_res = info_request.json()

    nickname = info_res.get('properties').get('nickname')
    email = info_res.get('kakao_account').get('email')

    # 해당 이메일을 사용해 가입한 이력이 있는지, 확인한다.

    # 해당 이메일로 가입한 이력이 없다면, 새로운 유저를 생성한다.
    user = User.objects.filter(email=email)
    if not user:
        user = User.objects.create_user(email=email, password='Kakao_' + nickname + '977')
        user.login_type = 1
        user.save()

        # 카카오 로그인의 경우 별도의 이메일 인증을 생략
        EmailAddress.objects.create(user=user, email=email, verified=True, primary=True)

        # 해당 유저의 정보를 업데이트한다. : login_type = 1 (카카오 로그인)
        # user Info 생성
        user_info, user_created = UserInfo.objects.get_or_create(user=user)
        new_user_point(user.id)  # 해당 유저의 포인트를 생성한다.

    #  소셜 로그인 정보는, 언제든 바뀔 수 았기 때문에 굳이 저장하지 않는다.
    kakao_profile = info_res.get('kakao_account').get('profile').get('profile_image_url')
    kakao_nickname = info_res.get('properties').get('nickname')

    # 로그인 응답 데이터 생성
    response_data = {
        'kakao_profile': kakao_profile,
        'kakao_nickname': kakao_nickname,
        'kakao_email': email,  # 로그인 처리를 위해 응답 데이터에 이메일을 포함시킨다.  / 비밀번호는 패턴화 되어있다. (Kakao_ + nickname + 977)
    }


    return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def kakao_test(request):
    code = request.data.get('code')
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
    }
    body = {
        'grant_type': 'authorization_code',
        'client_id': 'dcf8cc38ec4e7ec39baf6207a53ed140',
        'redirect_uri': 'http://localhost:8080/loading/',
        'code': code,
    }
    response = requests.post(headers=headers, url='https://kauth.kakao.com/oauth/token', data=body)
    pp(response.json())
    access_token = response.json().get('access_token')

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    }

    info_request = requests.get(url='https://kapi.kakao.com/v2/user/me', headers=headers)
    info_res = info_request.json()

    pp(info_res)

    return Response(data=info_res, status=status.HTTP_200_OK)
