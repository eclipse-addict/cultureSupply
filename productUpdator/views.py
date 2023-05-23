from .models import ProductUpdator, ProductUpdatorItems
from .serializers import ProductUpdatorSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse, JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from products.models import kicks as Product
from points.models import Point, PointHistory


class PostPageNumberPagination(PageNumberPagination):
    page_size = 5


class UpdatorViewSet(ModelViewSet):
    queryset = ProductUpdator.objects.prefetch_related('productUpdatorItems').order_by('-created_at')
    serializer_class = ProductUpdatorSerializer
    pagination_class = PostPageNumberPagination

    def get_queryset(self):
        user = self.request.query_params.get('user', None)
        condition = self.request.query_params.get('condition', None)
        condition = int(condition)
        if user:
            if condition == 0:
                print('request with user  condition == 0')
                return ProductUpdator.objects.prefetch_related('productUpdatorItems').filter(user=user).filter(final_approved=0).order_by('-created_at')
            elif condition == 1:
                print('request with user  condition == 1')
                return ProductUpdator.objects.prefetch_related('productUpdatorItems').filter(user=user).filter(final_approved=1).order_by('-created_at')
            elif condition == 2:
                print('request with user  condition == 2')
                return ProductUpdator.objects.prefetch_related('productUpdatorItems').filter(user=user).filter(final_approved=2).order_by('-created_at')
            else:
                print('request with user  condition == else')
                return ProductUpdator.objects.prefetch_related('productUpdatorItems').filter(user=user).order_by('-created_at')
        else:
            if condition == 0:
                return ProductUpdator.objects.prefetch_related('productUpdatorItems').filter(final_approved=0).order_by('-created_at')
            elif condition == 1:
                return ProductUpdator.objects.prefetch_related('productUpdatorItems').filter(final_approved=1).order_by('-created_at')
            elif condition == 2:
                return ProductUpdator.objects.prefetch_related('productUpdatorItems').filter(final_approved=2).order_by('-created_at')
            else:
                return ProductUpdator.objects.prefetch_related('productUpdatorItems').order_by('-created_at')
    def get_permissions(self):
        if 'user' in self.request.query_params:
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def create_updator(request):
    updatorItems = []
    brand, colorway, category, retail, date, local_imageUrl = None, None, None, None, None, None

    # Create a mutable copy of the request data
    data = request.data.copy()

    if data.get('brand'):
        brand = data.pop('brand')
    if data.get('color_select'):
        colorway = data.pop('color_select')
    if data.get('category'):
        category = data.pop('category')
    if data.get('retail'):
        retail = data.pop('retail')
    if data.get('date'):
        date = data.pop('date')
    if data.get('local_imageUrl'):
        local_imageUrl = data.pop('local_imageUrl')

    print(f'data : {data}')
    serializer = ProductUpdatorSerializer(data=data)

    if serializer.is_valid():
        updator = serializer.save()
    else:
        print(f'serializer.errors : {serializer.errors}')
        return HttpResponse(content={'message': 'fail'}, status=status.HTTP_400_BAD_REQUEST)

    if request.FILES:
        print('#' * 100)
        print(f'request.FILES : {request.FILES}')
        ProductUpdatorItems.objects.create(product_updator_id=updator,
                                           field_name='local_imageUrl',
                                           field_value='local_imageUrl',
                                           image=request.FILES['local_imageUrl'])

    if brand:
        updatorItems.append(ProductUpdatorItems(product_updator_id=updator, field_name='brand', field_value=brand))
    if colorway:
        updatorItems.append(
            ProductUpdatorItems(product_updator_id=updator, field_name='colorway', field_value=colorway))
    if category:
        updatorItems.append(
            ProductUpdatorItems(product_updator_id=updator, field_name='category', field_value=category))
    if retail:
        updatorItems.append(ProductUpdatorItems(product_updator_id=updator, field_name='retail', field_value=retail))
    if date:
        updatorItems.append(
            ProductUpdatorItems(product_updator_id=updator, field_name='release_date', field_value=date))

    if updatorItems:
        ProductUpdatorItems.objects.bulk_create(updatorItems)

    return HttpResponse(content={'message': 'success'}, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def accept_updator(request, pk):
    updator = ProductUpdator.objects.get(pk=pk)
    updator_items = ProductUpdatorItems.objects.filter(product_updator_id=updator)
    product = Product.objects.get(pk=updator.product.id)
    point = Point.objects.get(user=updator.user)

    for item in updator_items:
        if item.field_name == 'local_imageUrl':
            product.local_imageUrl = item.image
        elif item.field_name == 'brand':
            product.brand = item.field_value.strip("[, ], '")
        elif item.field_name == 'category':
            product.category = item.field_value.strip("[, ], '")
        elif item.field_name == 'colorway':
            product.colorway = item.field_value.strip("[, ], '")
        elif item.field_name == 'retail':
            product.retailPrice = item.field_value.strip("[, ], '")
        elif item.field_name == 'date':
            product.release_date = item.field_value.strip("[, ], '")

    updator_items.update(approved=True)
    product.save()
    print(f'after save product : {type(product.local_imageUrl)}')
    updator.final_approved = True
    updator.save()

    point.current_points += len(updator_items) * 100
    point.save()

    PointHistory.objects.create(user=updator.user, point_type='Product_update', point_amount=len(updator_items) * 100,
                                description='상품 업데이트 승인')

    return HttpResponse(content={'message': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def deny_updator(request, pk):
    updator = ProductUpdator.objects.get(pk=pk)
    updator.final_approved = 2 # 2 : denied
    updator.save()

    return HttpResponse(content={'message': 'success'}, status=status.HTTP_200_OK)
