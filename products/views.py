from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user, get_user_model
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from .serializers import kicksSerializer
from .models import kicks
from datetime import date, timedelta
import pprint
import requests
import json
import urllib.request as req
from urllib.parse import urlparse
import chardet
import os
import time
from yarl import URL
from google_images_download import google_images_download   #importing the library
from bs4 import BeautifulSoup
from assets.brand_list import brand_list

User =  User = get_user_model()


class ProductPagination(CursorPagination):
    page_size = 20
    page_size_query_param = None
    max_page_size = 20
    ordering = '-releaseDate'

class ProductListViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = kicks.objects.all()
    serializer_class = kicksSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['$name']
    
    def get_queryset(self):
        queryset = kicks.objects.all()
        brand = self.request.GET.get('brand', None)
        releaseDate = self.request.GET.get('releaseDate', None)
            
        if releaseDate:
            release = releaseDate.split(',')
            if len(release) == 2:
                queryset = queryset.filter(Q(releaseDate__range=[release[0], release[1]]))
            elif len(release) == 1:
                queryset = queryset.filter(Q(releaseDate=release[0]))    
        else: 
            queryset = queryset.filter(Q(releaseDate__range=[date.today() - timedelta(days=15), date.today() + timedelta(days=15)]))
        
        if brand:
            brand = brand.split(',')
            q = Q()
            for b in brand:
                q.add(Q(brand__icontains=b), q.OR)
            queryset = queryset.filter(q)    
        return queryset


'''
returns 15 most recent drops (no paginations) -> for main page component
'''
def popular_release(request):
    if request.method == 'GET':
        product_list = kicks.objects.exclude(local_imageUrl='http://localhost:8000/media/images/defaultImg.png').order_by('-releaseDate')[0:12]
        
        serializer = kicksSerializer(product_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    
'''
메인 페이지용, 신제품 선택 def
최근 등록된 15개 중 사진 file 을 가지고있고, 그중 기대 리셀가가 가장 높은 제품 1종 Return 
'''
def main_img(request):
    if request.method == 'GET':
        product_list = kicks.objects.exclude(local_imageUrl='http://localhost:8000/media/images/defaultImg.png').order_by('-releaseDate', '-estimatedMarketValue')[:25]
        main_img = product_list[0]
        result = []
        for p in product_list:
            if main_img.estimatedMarketValue < p.estimatedMarketValue:
                main_img = p
                result.append(main_img)
        print(f'main_img : {result}')
        serializer = kicksSerializer(result[:2], many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)



'''
sneaker list v.0.1
TODO: Searching function needs to be added. 
'''
def get_sneaker(request): 
    page = request.GET.get("page")
    keyword = request.GET.get("keyword")
    brand = request.GET.get("brand")
    release = request.GET.get("release")
    # release = request.GET.get("release")
    
    if brand != 'All':
        brand = brand.split(',')
    # release = release.split(',')
    
    if release != 'default':
        release = release.split(',')
        
    sneaker_list = None
    paginator = None
    q = Q()
    today = date.today()
    
    if keyword == '' and brand == 'All' and release =='default' or not release:
        sneaker_list = kicks.objects.filter(releaseDate__range=[date.today() - timedelta(days=15), date.today() + timedelta(days=15)]).all().order_by('-releaseDate')
    else:
    #키워드 설정     
        if keyword != '':
            q.add(Q(name__icontains=keyword), q.AND)
        elif release != 'default':
            if len(release) == 2:
                q.add(Q(releaseDate__range=[release[0], release[1]]), q.AND)
            elif len(release) == 1:
                q.add(Q(releaseDate=release[0]), q.AND)
        elif brand != 'All':
            for b in brand:
                q.add(Q(brand__icontains=b), q.OR)

        sneaker_list = kicks.objects.filter(q).order_by('-releaseDate')
    
    if len(sneaker_list) >= 10:
        paginator = Paginator(sneaker_list, 20)
        
    elif 0 < len(sneaker_list) < 10:
        paginator = Paginator(sneaker_list, len(sneaker_list))
    else:
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
    sneakers = paginator.get_page(page)
    serializer = kicksSerializer(sneakers, many=True)
        
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_detail(request, id):
    kick = get_object_or_404(kicks, id=id)
    
    serializer = kicksSerializer(kick)
    print(f'res : {kick}')
    
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product_like(request, product_id, user_id):
    user = User.objects.get(pk=user_id)
    kick = kicks.objects.get(id=product_id)
    
    if kick.like_users.filter(id=user_id).exists():
            kick.like_users.remove(user)
            return JsonResponse({'message':'removed'}, status = status.HTTP_200_OK)
    else:
        kick.like_users.add(user)
        return JsonResponse({'message':'added'}, status = status.HTTP_200_OK)
















'''
sneakers Data paser v1.0.0

'''
pp = pprint.PrettyPrinter(indent=4)
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'utf-8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Origin': 'https://thesneakerdatabase.com',
    'app-platform': 'Iron',
    # 'Host': '',
    'referer': 'https://thesneakerdatabase.com/sneakers/6778a67b-669c-4c3e-8ca0-2d3f1c911a8b',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}
goat_headers = {
    'accept': '*/*',
    'accept-encoding': 'utf-8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Origin': 'https://www.goat.com',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

new_release_url = getattr(settings, 'NEW_RELEASE_URL', None)



# TODO: 카테고리 별 제품 파싱 :
# Sneakers : 1968 ~ 2023
# T-Shirts : 1990 ~ 2023 
# Apparel : 1970 ~ 2023
# Hoodies : 2018 ~ 2022
# Outerwear : 1982 ~ 2023
# Bottoms : 1983 ~ 2023
# Bags : 1999 ~ 2023
# Jewelry : 1969 ~ 2023

def goat_collections(request):
    start = time.time()
    new_cnt = 0
    
    for j in range(7):
        for i in range(1, 200):
            url_list = [ 
            # f'https://ac.cnstrc.com/browse/group_id/all?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=11&page={i}&num_results_per_page=200&sort_by=relevance&sort_order=descending&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670821087867',
            f'https://ac.cnstrc.com/browse/group_id/all?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=11&page={i}&num_results_per_page=200&filters[recently_released]=sneakers&sort_by=release_date&sort_order=descending&fmt_options[hidden_fields]=gp_lowest_price_cents_3&fmt_options[hidden_fields]=gp_instant_ship_lowest_price_cents_3&fmt_options[hidden_facets]=gp_lowest_price_cents_3&fmt_options[hidden_facets]=gp_instant_ship_lowest_price_cents_3&_dt=1670822296441',
            f'https://ac.cnstrc.com/browse/group_id/all?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=11&page={i}&num_results_per_page=200&filters[recently_released]=apparel&sort_by=date_added&sort_order=descending&fmt_options[hidden_fields]=gp_lowest_price_cents_3&fmt_options[hidden_fields]=gp_instant_ship_lowest_price_cents_3&fmt_options[hidden_facets]=gp_lowest_price_cents_3&fmt_options[hidden_facets]=gp_instant_ship_lowest_price_cents_3&_dt=1670822445157',
            f'https://ac.cnstrc.com/browse/collection_id/new-arrivals-apparel?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=12&page={i}&num_results_per_page=200&filters%5Bproduct_condition%5D=new_no_defects&sort_by=relevance&sort_order=descending&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670910536899',
            f'https://ac.cnstrc.com/browse/collection_id/just-dropped?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=12&page={i}&num_results_per_page=200&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670910906505',
            f'https://ac.cnstrc.com/browse/collection_id/women-s-sneakers?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=12&page={i}&num_results_per_page=200&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670910951588',
            f'https://ac.cnstrc.com/browse/collection_id/toddler?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=12&page={i}&num_results_per_page=200&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670910987178',
            f'https://ac.cnstrc.com/browse/collection_id/most-wanted-new?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=12&page={i}&num_results_per_page=200&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670911039677',]
            
            url_list_name =['popular_release', 'recent_kicks', 'recent_apparel', 'newe_in', 'just_drop', 'womens', 'toddler', 'most_wanted',]
            
            response = requests.get(url=url_list[j], headers=goat_headers)
            print('res: ', response.status_code)
            # print('res: ', response.text)
            json_data = json.loads(response.text)
            products_list = json_data.get('response').get('results')
            
            if not products_list:
                print(f'No more products on {url_list_name[j]} found finished at page : {i}page.')
                break
            
            for p in range(len(products_list)):
                brand = products_list[p]['data'].get('brand')
                new_cnt += create_new_kick_data(products_list, p, brand)
            
    print(f'total New product count = {new_cnt}')
    print(f'time check : {time.time() - start}')
    
    return HttpResponse(status=status.HTTP_201_CREATED)
# 284,361 /200 = // current 21 page 
def get_goat(request):
    # request_URL = 'https://ac.cnstrc.com/browse/brand/air%20jordan?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=3&page=1&num_results_per_page=24&filters%5Brelease_date_year%5D=1985&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670597951900'
    # request_URL = 'https://ac.cnstrc.com/browse/brand/air%20jordan?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=4&page=1&num_results_per_page=200&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670599038050'
    # 아래 url 에 브랜드 이름을 바꿔서 요청을 구현 
    #브랜드 이름 리스트로 만들기. 
    start = time.time()
    new_cnt = 0
    for brand in brand_list: # brand 먼저 픽스 
        for i in range(1, 300):
            all_year_by_brand_url = f'https://ac.cnstrc.com/browse/group_id/all?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=9&page={i}&num_results_per_page=200&filters%5Brelease_date_year%5D=2022&filters%5Brelease_date_year%5D=2021&filters%5Brelease_date_year%5D=2020&filters%5Brelease_date_year%5D=2018&filters%5Brelease_date_year%5D=2019&filters%5Brelease_date_year%5D=2017&filters%5Brelease_date_year%5D=2016&filters%5Brelease_date_year%5D=2023&filters%5Brelease_date_year%5D=2015&filters%5Brelease_date_year%5D=2014&filters%5Brelease_date_year%5D=2013&filters%5Brelease_date_year%5D=2012&filters%5Brelease_date_year%5D=2011&filters%5Brelease_date_year%5D=2010&filters%5Brelease_date_year%5D=2008&filters%5Brelease_date_year%5D=2009&filters%5Brelease_date_year%5D=2006&filters%5Brelease_date_year%5D=2007&filters%5Brelease_date_year%5D=2005&filters%5Brelease_date_year%5D=2004&filters%5Brelease_date_year%5D=2002&filters%5Brelease_date_year%5D=2003&filters%5Brelease_date_year%5D=2001&filters%5Brelease_date_year%5D=2000&filters%5Brelease_date_year%5D=1999&filters%5Brelease_date_year%5D=1998&filters%5Brelease_date_year%5D=1997&filters%5Brelease_date_year%5D=1996&filters%5Brelease_date_year%5D=1985&filters%5Brelease_date_year%5D=1986&filters%5Brelease_date_year%5D=1989&filters%5Brelease_date_year%5D=1991&filters%5Brelease_date_year%5D=1993&filters%5Brelease_date_year%5D=1995&filters%5Brelease_date_year%5D=1994&filters%5Brelease_date_year%5D=1992&filters%5Brelease_date_year%5D=1990&filters%5Brelease_date_year%5D=1988&filters%5Bbrand%5D={brand.lower()}&sort_by=gp_lowest_price_cents_3&sort_order=ascending&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670814405023'
            # https://ac.cnstrc.com/browse/group_id/all?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=9&page=1&num_results_per_page=24&filters%5Brelease_date_year%5D=2022&filters%5Brelease_date_year%5D=1985&filters%5Brelease_date_year%5D=1986&filters%5Brelease_date_year%5D=1991&filters%5Brelease_date_year%5D=1992&filters%5Brelease_date_year%5D=1994&filters%5Brelease_date_year%5D=1993&filters%5Bbrand%5D=air%20jordan&sort_by=gp_lowest_price_cents_3&sort_order=descending&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670814405023'
            # request_URL = f'https://ac.cnstrc.com/browse/group_id/all?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=5&page={i}&num_results_per_page=200&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670600851575'
            # print(all_year_by_brand_url)
            response = requests.get(url=all_year_by_brand_url, headers=goat_headers)
            print('res: ', response.status_code)
            # print('res: ', response.text)
            json_data = json.loads(response.text)
            products_list = json_data.get('response').get('results')
            total_num_results = json_data.get('response').get('total_num_results')
            # print('products_list: ', products_list[0]['data'])
            # print('products_list: ', len(products_list))
            if not products_list:
                print(f'Nomore products found. {brand} finished at page : {i}page.')
                break
            
            for p in range(len(products_list)):
                new_cnt += create_new_kick_data(products_list, p, brand)
                
            print(f'new page Count = {i} // new Product Count: {new_cnt}')
    print(f'total New product count = {new_cnt}')
    print(f'time check : {time.time() - start}')

    return HttpResponse(status=status.HTTP_201_CREATED)

def create_new_kick_data(products_list, p, brand):
    print(f"products_list[p]['value']: {brand} {products_list[p].get('value')}")
    try:
        if not products_list[p]['data'].get('sku'):
            print(f'No sku found for {products_list[p].get("name")}')
            return 0
            
        else: 
            sku = products_list[p]['data'].get('sku')
            new_sku = str(sku).replace(' ', '-')
            print(f'sku check : {new_sku}')
            kick = kicks.objects.get(sku=new_sku) # 없으면 여기서 에러 발생 -> except 로
            print('Already exists') # 있으면 .
            
            result = 0
            
            # if not kick.brand:
            #     print(f'product brand updated : {kick.name}')
            #     kick.brand = brand
            #     result =1
            
            if not kick.releaseDate:
                print(f'product releaseDate updated : {kick.name}')
                if not products_list[p]['data'].get('release_date'):
                    print(f'No release date found for {products_list[p].get("name")}')
                else:
                    kick.releaseDate = products_list[p]['data'].get('release_date') 
                    result =1
            
            if kick.releaseDate == '1900-00-00':
                print(f'product releaseDate updated : {kick.name}')
                if not products_list[p]['data'].get('release_date'):
                    print(f'No release date found for {products_list[p].get("name")}')
                else:
                    kick.releaseDate = products_list[p]['data'].get('release_date') 
                    result =1
                
            
            if not kick.category:
                print(f'product category updated : {kick.name}')
                kick.category = products_list[p]['data'].get('category')
                result =1
                
            if not kick.product_type:
                print(f'product product_type updated : {kick.name}')
                kick.product_type = products_list[p]['data'].get('product_type')
                result =1
            
            if not kick.retailPrice:
                print(f'product retailPrice updated : {kick.name}')
                kick.retailPrice = products_list[p]['data'].get('retail_price_cents')
                result = 1        
                                    
            if not kick.imageUrl:
                print(f'product image_url updated : {kick.name}')
                kick.imageUrl = products_list[p]['data'].get('image_url')
                result = 1                            

            if result >0:
                kick.save()
                return 1
        
            return 0
    except kicks.DoesNotExist: # 존재하지 않는 제품이므로, 등록 처리
        #TODO: 신제품 등록시 사진 파일도 저장 처리 
        print(f'################New product######################')
        sku = products_list[p]['data'].get('sku')
        new_sku = str(sku).replace(' ', '-')
        kick = kicks(
                    uuid                 = products_list[p]['data'].get('id'),
                    name                 = products_list[p].get('value'),
                    brand                = brand,
                    category             = products_list[p]['data'].get('category'),
                    product_type         = products_list[p]['data'].get('product_type'),
                    colorway             = products_list[p]['data'].get('color'),                  
                    releaseDate          = products_list[p]['data'].get('release_date'),
                    release_date_year    = products_list[p]['data'].get('release_date_year'),
                    retailPrice          = products_list[p]['data'].get('retail_price_cents'),
                    retailPriceKrw       = products_list[p]['data'].get('retail_price_cents_krw'),
                    sku                  = new_sku,
                    imageUrl             = products_list[p]['data'].get('image_url'),
                    slug                 = products_list[p]['data'].get('slug')

            )
        kick.save()
        
        return 1 



def new_release_paser(request):
    
    response = requests.get(url=new_release_url, headers=headers)
    print(response.status_code)

    new_cnt = 0
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.select_one('#__NEXT_DATA__').get_text()
        json_data = json.loads(data)
        products_list = json_data['props']['pageProps']['newReleases']
    
    for p in range(len(products_list)):
        new_cnt += create_new_kick_data(products_list, p)
    print(f'new Count = {new_cnt}')
    return HttpResponse(status= status.HTTP_201_CREATED)
    # return JsonResponse(json_data['props']['pageProps']['newReleases'], safe=False)


def sneaker_datasneaker_data_by_year_paser_by_brand_paser(request):
    
    response = requests.get(url=new_release_url, headers=headers)
    json_data = json.loads(response.text)
    products_list = json_data['data']
    
    for p in range(len(products_list)):
        create_new_kick_data(products_list, p)

    return HttpResponse(status= status.HTTP_201_CREATED)



def sneaker_data_by_brand_paser(request):
    j_url_m = getattr(settings, 'J_URL_M', None)
    j_url_f = getattr(settings, 'J_URL_F', None)
    n_url_m = getattr(settings, 'N_URL_M', None)
    n_url_f = getattr(settings, 'N_URL_M', None)
    

    cnt = 0
    response = requests.get(url=n_url_f, headers=headers)
    json_data = json.loads(response.text)
    products_list = json_data['data']
    
    for p in range(len(products_list)):
        cnt += create_new_kick_data(products_list, p)
    
    print(f'new Count : {cnt}')
    
    return HttpResponse(status= status.HTTP_201_CREATED)


#update Count : 4849
def sneaker_img_paser(request):
    start = time.time()
    count = 0
    # 이미 추가한 것 필터로 빼고 갖고오기..
    all_products = kicks.objects.filter(local_imageUrl='http://localhost:8000/media/images/defaultImg.png').exclude(imageUrl__isnull=True).order_by('-releaseDate')
    
    for i, p in enumerate(all_products):
        
        if p.imageUrl!='' and p.imageUrl.find('stockx')== -1:
            print(f'Name check (goat):{p.id} {p.name}')
            print(f'URL Check:{p.imageUrl}')
            imageUrl = p.imageUrl
            # path = os.path.dirname(imageUrl)[22:]
            # 저장 경로 
            file_name = os.path.basename(imageUrl)
            path = urlparse(imageUrl).path
            path_url = path[:path.find(file_name)]
            
            
            # 디렉토리가 없으면 생성
            # check_dir(local_path)
            # 설정한 경로에 파일 저장
            try:                
                req.urlretrieve(imageUrl, '/Users/isaac/Desktop/Project/culturesupply/media/images/sneakers/'+file_name)
                # 해당 제품 db 업데이트
                img_url = 'http://localhost:8000/media/images/sneakers/'+file_name
                p.local_imageUrl = img_url
                ################################################################################################
                # smallImageUrl = p.smallImageUrl
                # # 저장 할 제품 이름
                # file_name = os.path.basename(smallImageUrl)
                # path = urlparse(smallImageUrl).path
                # path_url = path[:path.find(file_name)]
                # 저장 경로 
                local_path = '/Users/isaac/Desktop/Project/culturesupply/media/images/sneakers'+path_url
                # 디렉토리가 없으면 생성
                # check_dir(local_path)
                # 설정한 경로에 파일 저장 
                # req.urlretrieve(smallImageUrl, '/Users/isaac/Desktop/Project/culturesupply/media/images/sneakers/'+file_name)
                # # 해당 제품 db 업데이트
                # small_img_url = 'http://localhost:8000/media/images/sneakers/'+file_name
                # p.local_smallImageUrl = small_img_url
                ################################################################################################
                # thumbUrl = p.thumbUrl
                # # 저장 할 제품 이름
                # file_name = os.path.basename(thumbUrl)
                # path = urlparse(thumbUrl).path
                # path_url = path[:path.find(file_name)]
                # 저장 경로 
                # local_path = '/Users/isaac/Desktop/Project/culturesupply/media/images/sneakers'+path
                # # 디렉토리가 없으면 생성
                # # check_dir(local_path)
                # # 설정한 경로에 파일 저장 
                # req.urlretrieve(thumbUrl, '/Users/isaac/Desktop/Project/culturesupply/media/images/sneakers/'+file_name)
                # # 해당 제품 db 업데이트
                # thumb_Url_img_url = 'http://localhost:8000/media/images/sneakers/'+file_name

                # p.local_thumbUrl = thumb_Url_img_url
                # 최종 저장 
                p.save()
                count +=1
            except:
                print(f'Error occured')
                p.imageUrl = 'http://localhost:8000/media/images/defaultImg.png'
                p.save()
                
        # Stockx url 일 경우, 
        elif p.imageUrl!='' and p.imageUrl.find('stockx') >= 0:
            print(f'Name check (stockX) : {p.name}')
            opener = req.build_opener()
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            
            req.install_opener(opener)
            # encode : {'encoding': 'Windows-1252', 'confidence': 0.73, 'language': ''}
            print(f'encode : {chardet.detect(p.imageUrl.encode())}')
            imageUrl = p.imageUrl
            
            file_name = os.path.basename(imageUrl)
            path = urlparse(imageUrl).path
            path_url = path[:path.find(file_name)]
            # 저장 경로 
            local_path = '/Users/isaac/Desktop/Project/culturesupply/media/images/sneakers'+path
            # 저장 할 제품 이름
            file_name = os.path.basename(imageUrl)
            # 디렉토리가 없으면 생성
            # check_dir(local_path)
            # 설정한 경로에 파일 저장 
            try:                
                req.urlretrieve(imageUrl, '/Users/isaac/Desktop/Project/culturesupply/media/images/sneakers/'+file_name[:file_name.find('?')])
                # 해당 제품 db 업데이트
                img_url = 'http://localhost:8000/media/images/sneakers/'+file_name[:file_name.find('?')]
                p.local_imageUrl = img_url
                p.save()
                count +=1
            except:
                print(f'Error occured')
                p.imageUrl = 'http://localhost:8000/media/images/defaultImg.png'
                p.save()
                
    print(f'{time.time() - start}')
    return HttpResponse(status= status.HTTP_200_OK)

def check_dir(local_path):
    try : 
        if not os.path.exists(local_path):
            os.makedirs(local_path)
    except OSError:
        print(OSError.strerror)

def google_img_download(request):
    all_products = kicks.objects.filter(imageUrl='').order_by('-releaseDate')
    
    for p in all_products:
        response = google_images_download.googleimagesdownload()   #class instantiation
        arguments = {"keywords":p.name,
                    "limit":1,
                    "print_urls":True,
                    # "specific_site": "stockx.com/",
                    "image_directory": "images/sneakers/",
                    "output_directory": "media/"
                    }   
        
        try:
            paths = response.download(arguments)  
            
            raw_url = paths[0][list(paths[0].keys())[0]]

            print(f'final check2 : {"http://localhost:8000" + raw_url[0][raw_url[0].find("/media"):]}') #
            p.local_imageUrl = "http://localhost:8000" + raw_url[0][raw_url[0].find("/media"):]
            p.save()
                
        except Exception as error:
            print(f'error : {error}')
            continue

    
    return HttpResponse(status.HTTP_201_CREATED)

def duplicate_check(request):
    # q = Q()
    # q.add(Q(name__icontains='fear'))
    # all_products = kicks.objects.filter(name)
    # all_products = kicks.objects.filter(Q(name__icontains='fear')).order_by('-releaseDate')
    all_products = kicks.objects.all().exclude(sku__isnull=True).order_by('-releaseDate')
    for p in all_products:
        sku = p.sku
        # print(f'sku check : {sku}')
        if not sku :
            print(f'sku is NULL')
        else: 
            if sku.find('-') != -1:
                print(f'sku check "-" 있음: {sku}, {p.name}')
                new_sku = sku.replace('-', ' ') # 하이픈 없앤 형태로 중복 체크 
                # print(f'sku "-".strip : {new_sku}')
                duplicate = kicks.objects.filter(sku=new_sku)
                if duplicate :
                    print(f'sku duplicate : {duplicate[0].sku}')
                    print(f'sku duplicate : {duplicate[0].name}')
                    duplicate.delete()
            # else:
            #     print(f'sku check 없음 : {sku}')
            
    return HttpResponse(status.HTTP_200_OK)