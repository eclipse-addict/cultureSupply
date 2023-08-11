from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from products.models import kicks as Products
from .models import ApiInfo
from .serializers import ProductSerializer

User = get_user_model()


def api_key_validator(request):
    """
    API KEY 유효성 검사 및 호출 횟수 증가 함수
    Args:
        request:

    Returns:
        if api_key is valid:
            True
        else:
            False, Response
    """
    header_key = request.META.get("HTTP_API_KEY")
    if not header_key:
        response_data = {
            'status': '401',
            'message': 'API Key is required'
        }
        return False, Response(response_data, status=401)
    try:
        api_info = ApiInfo.objects.get(api_key=header_key)
    except ApiInfo.DoesNotExist:
        api_info = None
    except ValidationError:
        api_info = None

    if not api_info:
        response_data = {
            'status': '401',
            'message': 'Invalid API Key'
        }
        return False, Response(response_data, status=401)
    elif api_info.call_count >= 1000:
        response_data = {
            'status': '429',
            'message': 'API call limit exceeded'
        }
        return False, Response(response_data, status=429)
    else:
        api_info.call_count += 1
        api_info.save()

        return True, None


class ProductPagination(CursorPagination):
    page_size = 20
    page_size_query_param = None
    max_page_size = 20
    ordering = '-releaseDate'


class ApiProductListViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Products.objects.all()

        name_filter = self.request.query_params.get('name')
        release_date_start = self.request.query_params.get('release_date_start')
        release_date_end = self.request.query_params.get('release_date_end')

        if name_filter:
            queryset = queryset.filter(
                name__icontains=name_filter
            )

        if release_date_start and release_date_end:  # date range
            queryset = queryset.filter(releaseDate__gte=release_date_start, releaseDate__lt=release_date_end)

        elif release_date_start:  # single date filter
            queryset = queryset.filter(releaseDate=release_date_start)

        elif not release_date_start and not release_date_end:  # default date filter
            queryset = queryset.filter(releaseDate__gte=datetime.now() - timedelta(days=30))

        return queryset

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        # api_key 유효성 검사
        is_valid, response = api_key_validator(request)
        print(is_valid, response)
        if not is_valid:
            return response

        cache_key = f'product_list_{self.request.query_params}'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        response.data['request_query_params'] = request.query_params
        cache.set(cache_key, response.data, timeout=None)

        return response

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, pk=None):
        # api_key 유효성 검사
        is_valid, response = api_key_validator(request)
        if not is_valid:
            return response

        product = Products.objects.get(id=pk)
        if product:
            product.click += 1
            product.save()
        else:
            response_data = {
                'status': '404',
                'message': 'Product not found'
            }
            return Response(response_data, status=404)

        serializer = ProductSerializer(product)

        return Response(serializer.data)


"""
API 등록과 관련된 요청 
"""


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_register(request):
    """
    API 등록 요청
    Args:
        request:

    Returns:
        if success:
            Response
        else:
            Response
    """
    # print(request.data)
    print(request.user)
    user = request.user
    api_info, created = ApiInfo.objects.get_or_create(user=user)
    if created:
        response_data = {
            'status': '201',
            'message': 'API Key Successfully created',
        }
        return Response(response_data, status=201)
    else:
        response_data = {
            'status': '400',
            'message': 'API Key already exists',
        }
        return Response(response_data, status=400)


#TODO: API type 변경 요청 구현 필요
# 결제 시스템 연동 후 구현 이후 필요함.