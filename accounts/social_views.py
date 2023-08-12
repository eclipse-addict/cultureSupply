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
    response = requests.post(headers=headers, url= 'https://kauth.kakao.com/oauth/token', data=body)
    pp(response.json())
    access_token = response.json().get('access_token')

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    }

    """
    info_res: {'id': 2940814011, 'connected_at': '2023-08-11T00:45:04Z', 'properties': {'nickname': 'Isaac.S', 'profile_image': 'http://k.kakaocdn.net/dn/MlkP0/btshCgeMqEd/5KNgk1qLgROBX7mmZdrALK/img_640x640.jpg', 'thumbnail_image': 'http://k.k
    akaocdn.net/dn/MlkP0/btshCgeMqEd/5KNgk1qLgROBX7mmZdrALK/img_110x110.jpg'}, 'kakao_account': {'profile_nickname_needs_agreement': False, 'profile_image_needs_agreement': False, 'profile': {'nickname': 'Isaac.S', 'thumbnail_image_url': 'http
    ://k.kakaocdn.net/dn/MlkP0/btshCgeMqEd/5KNgk1qLgROBX7mmZdrALK/img_110x110.jpg', 'profile_image_url': 'http://k.kakaocdn.net/dn/MlkP0/btshCgeMqEd/5KNgk1qLgROBX7mmZdrALK/img_640x640.jpg', 'is_default_image': False}}}
    """
    info_request = requests.get(url='https://kapi.kakao.com/v2/user/me', headers=headers)
    info_res = info_request.json()

    pp(info_res)

    nickname = info_res.get('properties').get('nickname')
    email = info_res.get('kakao_account').get('email')


    # 해당 이메일을 사용해 가입한 이력이 있는지, 확인한다.

    # 해당 이메일로 가입한 이력이 없다면, 새로운 유저를 생성한다.
    user = User.objects.filter(email=email)
    if not user:
        user = User.objects.create_user(email=email, password='Kakao_'+nickname + '977')
        user.login_type = 1
        user.save()

        # 카카오 로그인의 경우 별도의 이메일 인증을 생략
        EmailAddress.objects.create(user=user, email=email, verified=True, primary=True)

    # 해당 유저의 정보를 업데이트한다. : login_type = 1 (카카오 로그인)
        print('새로운 유저가 생성되었습니다.')
        # user Info 생성
        user_info, user_created = UserInfo.objects.get_or_create(user=user)
        new_user_point(user.id)  # 해당 유저의 포인트를 생성한다.

    # 로그인 처리
    # login_res = requests.post(url='http://127.0.0.1:8000/user/dj-rest-auth/login/', data={'email': email, 'password': 'Kakao_'+nickname + '977'})
    login_res = requests.post(url='https://kickin.kr/user/dj-rest-auth/login/', data={'email': email, 'password': 'Kakao_'+nickname + '977'})
    pp(login_res)
    pp(login_res.json())
    login_res = login_res.json()

    #  소셜 로그인 정보는, 언제든 바뀔 수 았기 때문에 굳이 저장하지 않는다.
    kakao_profile = info_res.get('kakao_account').get('profile').get('profile_image_url')
    kakao_nickname = info_res.get('properties').get('nickname')

    # 로그인 응답 데이터 생성
    response_data = {
        'access_token': login_res.get('access_token'),
        'refresh_token': login_res.get('refresh_token'),
        'user': login_res.get('user'),
        'kakao_profile': kakao_profile,
        'kakao_nickname': kakao_nickname,

        # 필요한 경우 다른 사용자 정보도 포함시킬 수 있습니다.
    }

    print(f'access_token: {access_token}')
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
        'redirect_uri': 'https://kickin.kr/loading/',
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