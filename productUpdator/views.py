from .models import ProductUpdator, ProductUpdatorItems
from .serializers import ProductUpdatorSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse, JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def create_updator(request):
    updatorItems = []
    brand, colorway, category, retail, date, local_imageUrl = None, None, None, None, None, None

    if request.data.get('brand'):
        brand = request.data.pop('brand')
    if request.data.get('color_select'):
        colorway = request.data.pop('color_select')
    if request.data.get('category_select'):
        category = request.data.pop('category_select')
    if request.data.get('retail'):
        retail = request.data.pop('retail')
    if request.data.get('date'):
        date = request.data.pop('date')
    if request.data.get('local_imageUrl'):
        local_imageUrl = request.data.pop('local_imageUrl')

    print(f'request.data : {request.data}')
    serializer = ProductUpdatorSerializer(data=request.data)

    if serializer.is_valid():  # 에러 위치 확인 valid 통과를 하지 못함.
        updator = serializer.save()
    else:
        print(f'serializer.errors : {serializer.errors}')
        return HttpResponse(content={'message': 'fail'}, status=status.HTTP_400_BAD_REQUEST)

    if request.FILES:
        print('#'*100)
        print(f'request.FILES : {request.FILES}')
        ProductUpdatorItems.objects.create(product_updator_id=updator,
                                           field_name='local_imageUrl',
                                           field_value='local_imageUrl',
                                           image=request.FILES['local_imageUrl'])

    if brand:
        updatorItems.append(ProductUpdatorItems(product_updator_id=updator, field_name='brand', field_value=brand))
    if colorway:
        updatorItems.append(ProductUpdatorItems(product_updator_id=updator, field_name='colorway', field_value=colorway))
    if category:
        updatorItems.append(ProductUpdatorItems(product_updator_id=updator, field_name='category', field_value=category))
    if retail:
        updatorItems.append(ProductUpdatorItems(product_updator_id=updator, field_name='retail', field_value=retail))
    if date:
        updatorItems.append(ProductUpdatorItems(product_updator_id=updator, field_name='release_date', field_value=date))

    if updatorItems:
        ProductUpdatorItems.objects.bulk_create(updatorItems)


    return HttpResponse(content={'message': 'success'}, status=status.HTTP_201_CREATED)



class PostPageNumberPagination(PageNumberPagination):
    page_size = 20


class UpdatorViewSet(ModelViewSet):
    queryset = ProductUpdator.objects.prefetch_related('productUpdatorItems')
    serializer_class = ProductUpdatorSerializer
    pagination_class = PostPageNumberPagination
    permission_classes = [IsAdminUser]









