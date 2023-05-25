from django.shortcuts import render
from .serializers import RaffleSerializer, RaffleEntrySerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .models import Raffle, RaffleEntry
from products.models import kicks as Product

User = get_user_model()


class RafflePagination(PageNumberPagination):
    page_size = 10



class RaffleViewSet(viewsets.ModelViewSet):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = RafflePagination

    def create(self, request, *args, **kwargs):
        print(request.data)
        product_id = request.data.get('product')
        product = Product.objects.get(pk=product_id)
        serializer = self.get_serializer( data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # product 필드에 대한 유효성 검사
        print(product_id)
        if not product_id:
            return Response({'product': ['이 필드는 필수 항목입니다!!!!']}, status=status.HTTP_400_BAD_REQUEST)

        # product_id에 해당하는 Product 객체가 존재하는지 확인하는 추가 로직
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'product': ['유효하지 않은 상품입니다.']}, status=status.HTTP_400_BAD_REQUEST)

        # product_id가 유효한 경우 serializer를 저장하고 응답 생성
        serializer.save(product=product)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class RaffleEntryViewSet(viewsets.ModelViewSet):
    queryset = RaffleEntry.objects.all()
    serializer_class = RaffleEntrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = RafflePagination

