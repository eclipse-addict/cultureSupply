from django.conf import settings 
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticated

from .models import Sneaker, Image
from .forms import SneakerForm
from .serializer.sneakers import SneakerListSerializer, SneakerDetailSerializer
from django.views.decorators.http import require_POST, require_safe, require_http_methods

class SneakerViewSet(ModelViewSet):
    queryset = Sneaker.objects.all()
    serializer_class = SneakerDetailSerializer
    permission_classes_by_action = {'list':           [AllowAny],
                                    'create':         [IsAuthenticated],
                                    'update':         [IsAuthenticated],
                                    'partial_update': [IsAuthenticated],
                                    'destroys':       [IsAuthenticated],
                                    
                                    }
    
    def get_permissions(self):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
        

sneaker_list = SneakerViewSet.as_view({
    'get': 'list',
    'post' : 'create',
})

sneaker_detail = SneakerViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})


import requests
import json
from pprint import pprint 

def test_req(request):
    
    query = 'jordan 1'
    
    url = f'https://stockx.com/api/browse?_search={query}&page=25'
    
    # url = 'https://stockx.com/sneakers/release-date?years=2022'

    headers = {
        'accept': 'application/json',
        'accept-encoding': 'utf-8',
        'accept-language': 'en-GB,en;q=0.9',
        'app-platform': 'Iron',
        'referer': 'https://stockx.com/en-gb',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    html = requests.get(url=url, headers=headers)
    output = json.loads(html.text)
    # http://localhost:8000/sneakers/sneaker/test
    # json.loads(response.text)
    # print('request result', html)
    # print('TEST RESULT :', html.text)
    

#    dict_keys(['id', 'uuid', 'brand', 'browseVerticals', 'category', 'charityCondition', 'colorway', 
# 'condition', 'countryOfManufacture', 'dataType', 'description', 'hidden', 'listingType', 'minimumBid', 
# 'gender', 'media', 'name', 'productCategory', 'releaseDate', 'releaseTime', 'belowRetail', 'retailPrice',
# 'shoe', 'shortDescription', 'styleId', 'tickerSymbol', 'title', 'traits', 'type', 'urlKey', 'year', 'market', 
# '_tags', 'lock_selling', 'selling_countries', 'buying_countries', 'hot_keywords_updated_date', 'product_importance_score', 
# 'calculated_display_title', 'hot_keywords', 'lowestAskThresholdMet', 'objectID'])

    print('TEST RESULT :', output['Products'][0]['brand'])
    
    return HttpResponse(html.text)