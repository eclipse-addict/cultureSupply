from .models import ProductUpdator, ProductUpdatorItems
from .serializers import productUpdatorSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.http import HttpResponse, JsonResponse
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
    print(f'reqeust.data : {request.data}')
    print(f'request.file : {request.FILES}')
    # updator_items = reqeust.data["updater_itmes"] # 받아서 -> 딕셔너리로 변환 -> 회문 돌면서 저장. 
    serializer = productUpdatorSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        updator = serializer.save()
        # print(f'serializer.data check : {request}')
        excluding_fields = ['id', 'product_updator']
        for name in request.data:
            print(f'name : {name}, value : {request.data[name]}')
            if name not in excluding_fields:
                if 'img' in name:
                    print(f'img : {request.data[name]}')
                    ProductUpdatorItems.objects.create(product_updator_id=updator, field_name=name, field_value=request.data[name], image=request.data[name])
                else:
                    print(f'not img : {request.data[name]}')
                    ProductUpdatorItems.objects.create(product_updator_id=updator, field_name=name, field_value=request.data[name])
    
    
    
    return HttpResponse(status=status.HTTP_201_CREATED) 


@api_view(['GET',])
@permission_classes([IsAdminUser])
def get_updator_list(request):
    """_summary_
        Since the updator is only be accepeted by admin, only admin can see the list of updators.
    Args:
        request (_type_): _description_
    """
    pass