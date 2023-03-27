from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user, get_user_model
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q, Avg, Count, Prefetch
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from .serializers import productListSerializer, productSerializer
from .models import kicks, productImg
from datetime import date, timedelta
import pprint
import requests
import json
import datetime
import urllib.request as req
from urllib.parse import urlparse
import chardet
import os
import time
from yarl import URL
from google_images_download import google_images_download   #importing the library
from bs4 import BeautifulSoup
from assets.brand_list import brand_list
from django.utils import timezone
from django_filters import rest_framework as filters
from reviews.models import Review
User =  User = get_user_model()


class ProductPagination(CursorPagination):
    page_size = 20
    page_size_query_param = None
    max_page_size = 20
    ordering = '-releaseDate'

class ProductFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter', label='Search')
    brand = filters.CharFilter(method='brand_filter', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category', lookup_expr='icontains')
    release_date = filters.CharFilter(method='release_date_filter', label='Release Date Range')
    info_registrequired = filters.CharFilter(method='info_registrequired_filter', label='Info_Regist_Required')

    class Meta:
        model = kicks
        fields = ('search', 'brand', 'category', 'release_date', 'info_registrequired')
        
    def search_filter(self, queryset, name, value):
        print('search_filter')
        keyword = value.replace('+', ' ')
        
        return queryset.filter(
            Q(name__icontains=keyword) | Q(name__icontains=keyword.replace(' ', '')))
        
    def brand_filter(self, queryset, name, value):
        print('brand_filter')
        brand_list = value.split(',')
        q = Q()
        for brand in brand_list:
            q.add(Q(brand__icontains=brand), Q.OR)
            
        queryset = queryset.filter(q)
        
        return queryset
        
    def release_date_filter(self, queryset, name, value):
        print('release_date_filter')
        if not value:
            print('releaseDate is null')
            return queryset.all().order_by('-releaseDate')
            # releaseDate가 null인 경우
        else:
            # releaseDate가 null이 아닌 경우
            date_range = value.split(',')
            if len(date_range) == 1: #if only 1 date provided, set it as both start and end date
                start_date = end_date = date_range[0]
            else:
                start_date = date_range[0]
                end_date = date_range[1]
            print(start_date, end_date)
        return queryset.filter(releaseDate__range=[start_date, end_date])

    def info_registrequired_filter(self, queryset, name, value):
        print('#'*30)
        print('info_registrequired_filter')
        print('#'*30)
        if value == 'true':
            return queryset.filter(
                Q(local_imageUrl__icontains='/media/images/defaultImg.png') | 
                Q(brand__isnull=True) | 
                Q(category__isnull=True) |
                Q(releaseDate__isnull=True) |
                Q(retailPrice__isnull=True) |
                Q(colorway__isnull=True) |
                Q(releaseDate__icontains='1900-01-01') 
                ).order_by('-releaseDate')
        else:
            return queryset.all()

class ProductListViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = kicks.objects.all()
    serializer_class = productListSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter




# class ProductListViewSet(generics.ListAPIView):
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     queryset = kicks.objects.all()
#     serializer_class = productListSerializer
#     pagination_class = ProductPagination
#     # filter_backends = [filters.SearchFilter]
#     filter_backends = [DjangoFilterBackend]
#     # search_fields = ['name']
    
#     def get_queryset(self):
#         queryset = kicks.objects.all()
#         search = self.request.GET.get('search')
#         brand = self.request.GET.get('brand', None)
#         releaseDate = self.request.GET.get('releaseDate', None)
        
#         if not releaseDate and not search and not brand :
#             queryset = queryset.filter(Q(releaseDate__range=[date.today() - timedelta(days=15), date.today() + timedelta(days=15)]))
        
#         if releaseDate:
#             release = releaseDate.split(',')
#             if len(release) == 2:
#                 queryset = queryset.filter(Q(releaseDate__range=[release[0], release[1]]))
#             elif len(release) == 1:
#                 queryset = queryset.filter(Q(releaseDate=release[0]))    
        
#         if search:
#             q = Q()
#             keyword = search.replace('+', ' ')
#             q.add(Q(name__icontains=keyword), q.OR) # 검색어 조건 공백 포함 검색
#             q.add(Q(name__icontains=keyword.replace(' ','')), q.OR) # 검색어 조건 공백 제거 후 붙여서 검색
#             # //TODO: 주석 처리 23.02.14 -> 검색 결과의 정확도가 떨어짐. ex) jordan 5 로 검색 시, jordan, 5 로 각각 검색한 결과까지 함께 결과에 포함됨. 
#             # for word in search.split():
#             #     q.add(Q(name__icontains=word), q.OR)
                
#             queryset = queryset.filter(q)
            
#         if brand:
#             brand = brand.split(',')
#             q = Q()
#             for b in brand:
#                 q.add(Q(brand__icontains=b), q.OR)
#             queryset = queryset.filter(q)
            
#         return queryset


'''
returns 15 most recent drops (no paginations) -> for main page component
'''
def popular_release(request):
    if request.method == 'GET':
        product_list = kicks.objects.exclude(local_imageUrl='http://localhost:8000/media/images/defaultImg.png').order_by('-releaseDate')[0:12]
        
        serializer = productSerializer(product_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    
'''
메인 페이지용, 신제품 선택 def
최근 등록된 15개 중 사진 file 을 가지고있고, 그중 기대 리셀가가 가장 높은 제품 1종 Return 
'''
def main_img(request):
    if request.method == 'GET':
        product_list = kicks.objects.exclude(local_imageUrl='http://localhost:8000/media/images/defaultImg.png').order_by('-releaseDate', '-estimatedMarketValue')[:25]
        main_img = product_list[0]
        result = []
        for p in product_list:
            if main_img.estimatedMarketValue < p.estimatedMarketValue:
                main_img = p
                result.append(main_img)
        print(f'main_img : {result}')
        serializer = productListSerializer(result[:2], many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_detail(request, id):
    kick = get_object_or_404(kicks.objects.prefetch_related(
        Prefetch('reviews', queryset=Review.objects.annotate(
            like_count=Count('like_users'),
            dislike_count=Count('dislike_users')
        ))), id=id)
    serializer = productSerializer(kick)
    print(f'res : {serializer.data}')
    return Response(serializer.data)
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_detail(request, id):
#     kick = get_object_or_404(kicks, id=id)
    
#     serializer = productSerializer(kick)
#     print(f'res : {kick}')
    
#     return JsonResponse(serializer.data, safe=True)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_like(request, product_id, user_id):
    user = User.objects.get(pk=user_id)
    kick = kicks.objects.get(id=product_id)
    
    if kick.like_users.filter(id=user_id).exists():
            kick.like_users.remove(user)
            return JsonResponse({'message':'removed'}, status = status.HTTP_200_OK)
    else:
        kick.like_users.add(user)
        return JsonResponse({'message':'added'}, status = status.HTTP_200_OK)
