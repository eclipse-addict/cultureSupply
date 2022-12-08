from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user, get_user_model
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from .serializers import kicksReviewSerializer
from .models import Review
from products.models import kicks as Product
from accounts.models import UserInfo
User =  User = get_user_model()



@api_view(['GET',])
@permission_classes([AllowAny])
def get_review_list(reqeust, product_id):
    product = Product.objects.get(pk=product_id) # product 가져오기.
    review_list = Review.objects.filter(product=product).order_by('-created_at')
    serializer = kicksReviewSerializer(review_list, many=True)
    
    return JsonResponse(serializer.data, safe=False)




@api_view(['POST', 'PUT',])
@permission_classes([IsAuthenticated])
def create_review(request, product_id, user_id):
    user = User.objects.get(pk=user_id) # request user
    product = Product.objects.get(pk=product_id) # product 가져오기. 
    user_info = UserInfo.objects.get(user_id=user_id)
    print(f'User: {user}')
    print(f'user_info: {user_info.id}')
    
    review = None
    if request.method == 'POST':
        review = Review.objects.filter(user_id=user, product_id=product)
        if review:
            print(f'You Already have a Review on this Product')
            return HttpResponse({'message': 'You Already have a Review on this Product'}, status=status.HTTP_409_CONFLICT)
        else: 
            print(f'Create Review for {product.name}')
            serializer = kicksReviewSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                print('Create Review!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                serializer.save(user_info=user_info, user=user, product=product)
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            
            
    elif request.method == 'PUT': # update review 
        pass
    