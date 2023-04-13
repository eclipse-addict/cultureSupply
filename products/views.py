from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user, get_user_model
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
# from django.core.paginator import Paginator
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
# from datetime import date, timedelta
# import pprint
# import requests
# import json
# import datetime
# import urllib.request as req
# from urllib.parse import urlparse
# import chardet
# import os
# import time
# from yarl import URL
from google_images_download import google_images_download   #importing the library
# from bs4 import BeautifulSoup
from assets.brand_list import brand_list
# from django.utils import timezone
from django_filters import rest_framework as filters
from reviews.models import Review
from django.db import connection, reset_queries


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







'''
returns 15 most recent drops (no paginations) -> for main page component
'''
def recent_releases(request):
    if request.method == 'GET':
        product_list = kicks.objects.exclude(local_imageUrl='media/images/defaultImg.png').exclude(releaseDate__isnull=True).order_by('-releaseDate')[:15]
        
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
    reset_queries()
    kick = get_object_or_404(kicks.objects.prefetch_related(
        Prefetch('reviews', queryset=Review.objects.annotate(
            like_count=Count('like_users'),
            dislike_count=Count('dislike_users')
        ))), id=id)
    
    query_info = connection.queries
    for query in query_info:
        print(query['sql'])
        
    serializer = productSerializer(kick)
    print(f'res : {serializer.data}')
    return Response(serializer.data)




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

# def get_sql_queries(original_func):
# 	def wrapper(*args, **kwargs):
# 		reset_queries()
# 		original_func(*args, **kwargs)
# 		query_info = connection.queries
# 		for query in query_info:
# 			print(query['sql'])
# 		return wrapper



# @get_sql_queries
# def select_all_test(request): 
#     print('select_all_test')
#     reset_queries()
#     test_list = kicks.objects.all()
#     for i in range(2):
#         print(test_list[i])
    
#     query_info = connection.queries
#     for query in query_info:
#         print(query['sql'])
        
#     return JsonResponse({'message':'success'}, status = status.HTTP_200_OK)
