from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializers import RaffleSerializer, RaffleEntrySerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .models import Raffle, RaffleEntry
from products.models import kicks as Product

User = get_user_model()


class RafflePagination(PageNumberPagination):
    page_size = 3



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
            print('Create Raffle!!!!!!!!!!!!!!!!!!!')
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('Create Raffle Failed!!!!!!!!!!!!!!!!!!!')
            print(serializer.errors)

    def retrieve(self, request, pk=None):
        print('Retrieve Raffle!!!!!!!!!!!!!!!!!!!')
        try:
            raffle = get_object_or_404(Raffle.objects.filter(product=pk))
            return JsonResponse(data={'result': '1'}, status=status.HTTP_200_OK)
        except:
            return JsonResponse(data={'result': '0'}, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def raffle_entry(request):
    if request.method == 'POST':
        print('Raffle Entry!!!!!!!!!!!!!!!!!!!')
        user = request.user
        raffleEntry = RaffleEntry.objects.filter(user=user, raffle=request.data.get('raffle'))

        if raffleEntry:
            return JsonResponse(data={'message': '이미 응모하신 제품입니다.'}, status=status.HTTP_302_FOUND)
        else:
            raffle_id = request.data.get('raffle')
            raffle = Raffle.objects.get(pk=raffle_id)
            raffle_entry = RaffleEntry.objects.create(user=user, raffle=raffle)
            raffle_entry.save()
            return JsonResponse(data={'result': '응모가 완료되었습니다.'}, status=status.HTTP_201_CREATED)

