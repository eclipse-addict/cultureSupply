from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user, get_user_model
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from .serializers import kicksReviewSerializer
from .models import Review
from ..products.models import kicks as Product

User =  User = get_user_model()


@api_view(['POST', 'PUT',])
@permission_classes([IsAuthenticated])
def create_review(request, product_id, user_id):
    user = User.objects.get(pk=user_id) # request user
    product = Product.objects.get(pk=product_id) # product 가져오기. 
    review = None
    if request.method == 'POST':
        try:
            review = Review.objects.filter(user=user, product=product)
            print(f'You Already have a Review on this Product')
            return HttpResponse({'message': 'You Already have a Review on this Product'}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            print(f'Create Review for {product.name}')
            serializer = kicksReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user, product=product)
                return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'PUT': # update review 
        pass
    