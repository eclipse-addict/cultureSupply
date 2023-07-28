from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user, get_user_model
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
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
from .serializers import ProductSerializer, RecentReleaseSerializers, ProductDetailSerializer
from .models import kicks, productImg, ProductCrawlingFlag
from google_images_download import google_images_download
from assets.brand_list import brand_list
from django_filters import rest_framework as filters
from django.core.cache import cache
from reviews.models import Review
import re
import time
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

User = get_user_model()


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
    ordering = filters.CharFilter(method='order_filter', label='order_filter')

    class Meta:
        model = kicks
        fields = ('search', 'brand', 'category', 'release_date', 'info_registrequired', 'ordering')

    def order_filter(self, queryset, name, value):
        print('main_page_filter')
        if value == 'click':
            print('Order by Click')
            ProductPagination.ordering = '-click'

        elif value == 'most_commented':
            print('Order by most_hyped')
            queryset = queryset.annotate(review_count=Count('reviews')).order_by('-review_count')
            ProductPagination.ordering = '-review_count'

        else:
            print('Order by recent_drop')
            ProductPagination.ordering = '-releaseDate'

        return queryset

    def search_filter(self, queryset, name, value):
        keyword = value.replace('+', ' ')
        keyword_regex = re.sub(r'\s+', r'\\s*', keyword)

        # Add space between the letters in the keyword if they are not already separated by space
        keyword_with_space = re.sub(r'(?<=\D)(?=\d)|(?<=\d)(?=\D)', ' ', keyword)

        return queryset.filter(
            Q(name__icontains=keyword) |
            Q(name__iregex=fr'{keyword_regex}') |
            Q(name__icontains=keyword_with_space))

    def brand_filter(self, queryset, name, value):
        brand_list = value.split(',')
        q = Q()
        for brand in brand_list:
            q.add(Q(brand__icontains=brand), Q.OR)

        queryset = queryset.filter(q)

        return queryset

    def release_date_filter(self, queryset, name, value):
        if not value:
            return queryset.order_by('-releaseDate')
        else:
            date_range = value.split(',')
            if len(date_range) == 1:
                start_date = end_date = date_range[0]
            else:
                start_date = date_range[0]
                end_date = date_range[1]
        return queryset.filter(releaseDate__range=[start_date, end_date])

    def info_registrequired_filter(self, queryset, name, value):
        if value:
            value_list = value.split(',')

            q = Q()

            if len(value_list) == 5:
                print('all condition')
                q &= (Q(brand__isnull=True) | Q(category='') | (Q(releaseDate__isnull=True) | Q(releaseDate='1900-00-00') | Q(releaseDate='1970-01-01')) | Q(retailPrice__isnull=True) | Q(retailPrice=0) | Q(local_imageUrl__icontains='defaultImg.png'))

                return queryset.filter(q).order_by('-releaseDate')

            for value in value_list:
                if value == 'brand':
                    q &= Q(brand__isnull=True)
                elif value == 'category':
                    q &= Q(category='')
                elif value == 'date':
                    q &= (Q(releaseDate__isnull=True) |
                          Q(releaseDate='1900-00-00') |
                          Q(releaseDate='1970-01-01'))
                elif value == 'price':
                    q &= Q(retailPrice__isnull=True) | Q(retailPrice=0)
                elif value == 'image':
                    q &= Q(local_imageUrl__icontains='defaultImg.png')

            return queryset.filter(q).order_by('-releaseDate')
        else:
            return queryset.order_by('-releaseDate')


class ProductListViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # queryset = kicks.objects.prefetch_related('like_users')
    # queryset = kicks.objects.prefetch_related('reviews',
    #                                           'like_users').annotate(review_count=Count('reviews'),
    #                                                                  like_count=Count('like_users'),
    #                                                                  rating_avg=Avg('reviews__rating'))
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = kicks.objects.all()

        name_filter = self.request.query_params.get('name')
        release_date_start = self.request.query_params.get('release_date_start')
        release_date_end = self.request.query_params.get('release_date_end')

        if name_filter:
            queryset = queryset.filter(
                name__icontains=name_filter
            )

        if release_date_start and release_date_end:
            queryset = queryset.filter(
                releaseDate__range=(release_date_start, release_date_end)
            )


        queryset = queryset.prefetch_related(
            Prefetch('like_users', queryset=User.objects.only('id'))
        )

        return queryset


    def list(self, request, *args, **kwargs):
        start_time = time.time()

        cache_key = f'product_list_{self.request.query_params}'
        print('cache_key', cache_key)
        cached_data = cache.get(cache_key)

        if cached_data is not None:

            print('cache hit')
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution Time with cache: {execution_time} seconds")
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        response.data['request_query_params'] = request.query_params
        cache.set(cache_key, response.data, timeout=None)

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Execution Time: {execution_time} seconds")
        print(f"Execution Time: {execution_time} seconds")

        return response


'''
for main page component
'''
@api_view(['GET'])
@permission_classes([AllowAny])
def get_detail(request, prd_id):
    kick = kicks.objects.prefetch_related('reviews',
                                          'like_users').annotate(review_count=Count('reviews'),
                                                                 like_count=Count('like_users'),
                                                                 rating_avg=Avg('reviews__rating')).get(pk=prd_id)

    # 조회수 증가
    kick.click += 1
    kick.save()
    serializer = ProductDetailSerializer(kick)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_like(request, product_id, user_id):
    user = User.objects.get(pk=user_id)
    kick = kicks.objects.get(id=product_id)

    if kick.like_users.filter(id=user_id).exists():
        kick.like_users.remove(user)
        return JsonResponse({'message': 'removed'}, status=status.HTTP_200_OK)
    else:
        kick.like_users.add(user)
        return JsonResponse({'message': 'added'}, status=status.HTTP_200_OK)


from datetime import datetime
from pytz import timezone

# 최종 업데이트 일시 가져오기
@api_view(['GET'])
@permission_classes([AllowAny])
def get_last_updated(request):
    user_format = '%Y-%m-%d %H:%M:%S'
    last_updated = ProductCrawlingFlag.objects.latest('created_at').created_at
    formatted_time = last_updated.strftime(user_format)

    return JsonResponse({'last_updated': formatted_time}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def recent_releases(request):
    # get latest 10 products
    # release_date_start is 10 days ago
    # release_date_end is today
    release_date_end = datetime.now(timezone('Asia/Seoul'))
    release_date_start = release_date_end - timedelta(days=15)
    latest_products = kicks.objects.filter(releaseDate__range=(release_date_start, release_date_end)).order_by('-releaseDate')[:12]
    serializer = ProductSerializer(latest_products, many=True)
    return Response(serializer.data)
