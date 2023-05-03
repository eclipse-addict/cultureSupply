from .models import ProductUpdator, ProductUpdatorItems
from .serializers import productUpdatorSerializer
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
    """_summary_
        authenticated user can create a product updator which is a list of items to update.
    Args:
        reqeust (_type_): _description_
    """
    print(f'request : {request}')
    img_file = request.data.pop('local_imageUrl')
    # print(f'img_file : {img_file}')
    print(f'reqeust.data : {request.data}')
    print(f'request.file : {request.FILES}')
    # updator_items = reqeust.data["updater_itmes"] # 받아서 -> 딕셔너리로 변환 -> 회문 돌면서 저장. 
    serializer = productUpdatorSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        updator = serializer.save()

        if request.FILES:
            print('#'*100)
            print(f'request.FILES : {request.FILES}')
            ProductUpdatorItems.objects.create(product_updator_id=updator,
                                               field_name='local_imageUrl',
                                               field_value='local_imageUrl',
                                               image=request.FILES['local_imageUrl'])

        excluding_fields = ['user', 'product_id']
        for name in request.data:
            print(f'name : {name}, value : {request.data[name]}')
            if name not in excluding_fields:
                print(f'not img : {request.data[name]}')
                ProductUpdatorItems.objects.create(product_updator_id=updator,
                                                   field_name=name,
                                                   field_value=request.data[name])


    return HttpResponse(content={'message': 'success'}, status=status.HTTP_201_CREATED)



class PostPageNumberPagination(PageNumberPagination):
    page_size = 20


class UpdatorViewSet(ModelViewSet):
    queryset = ProductUpdator.objects.prefetch_related('productUpdatorItems')
    serializer_class = productUpdatorSerializer
    pagination_class = PostPageNumberPagination
    permission_classes = [IsAdminUser]









