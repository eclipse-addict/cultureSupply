from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from .models import kicks
from django.conf import settings
from .serializers import kicksSerializer
import pprint
import requests
import json

'''
sneakers Data paser v1.0.0

'''
pp = pprint.PrettyPrinter(indent=4)
headers = {
    'accept': 'application/json',
    'accept-encoding': 'utf-8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Origin': 'https://thesneakerdatabase.com',
    'app-platform': 'Iron',
    'Host': 'www.thesneakerdatabase.com',
    'referer': 'https://stockx.com/en-gb',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

new_release_url = getattr(settings, 'NEW_RELEASE_URL', None)


def create_new_kick_data(products_list, p):
    print('new_release_url : ', new_release_url)
    try:
        kicks.objects.get(sku=products_list[p]['sku'])
        print('Already exists')
    except kicks.DoesNotExist:
            # 존재하지 않는 제품이므로, 등록 처리
        print('New product')
        kick = kicks(
                    uuid                 = products_list[p]['_id'],
                    brand                = products_list[p]['brand'],
                    colorway             = products_list[p]['colorway'],                    
                    gender               = products_list[p]['gender'],
                    description          = products_list[p]['story'],
                    name                 = products_list[p]['name'],
                    releaseDate          = products_list[p]['releaseDate'],
                    retailPrice          = products_list[p]['retailPrice'],
                    estimatedMarketValue = products_list[p]['estimatedMarketValue'],
                    sku                  = products_list[p]['sku'],
                    imageUrl             = products_list[p]['image']['original'],
                    smallImageUrl        = products_list[p]['image']['small'],
                    thumbUrl             = products_list[p]['image']['thumbnail'],
            )
        kick.save()
        


def new_release_paser(request):
    
    response = requests.get(url=new_release_url, headers=headers)
    print('res: ', response.status_code)
    json_data = json.loads(response.text)
    products_list = json_data['data']
    
    for p in range(len(products_list)):
        create_new_kick_data(products_list, p)

    return HttpResponse(status= status.HTTP_201_CREATED)



def sneaker_datasneaker_data_by_year_paser_by_brand_paser(request):
    
    response = requests.get(url=new_release_url, headers=headers)
    json_data = json.loads(response.text)
    products_list = json_data['data']
    
    for p in range(len(products_list)):
        create_new_kick_data(products_list, p)

    return HttpResponse(status= status.HTTP_201_CREATED)


# TODO: .env 
def sneaker_data_by_brand_paser(request):
    j_url_m = getattr(settings, 'J_URL_M', None)
    j_url_f = getattr(settings, 'J_URL_F', None)
    n_url_m = getattr(settings, 'N_URL_M', None)
    n_url_f = getattr(settings, 'N_URL_M', None)
    
    response = requests.get(url=n_url_m, headers=headers)
    json_data = json.loads(response.text)
    products_list = json_data['data']
    
    for p in range(len(products_list)):
        try:
            kicks.objects.get(sku=products_list[p]['sku'])
            print('Already exists')
        except kicks.DoesNotExist:
            # 존재하지 않는 제품이므로, 등록 처리
            print('New product')
            kick = kicks(
                        uuid                 = products_list[p]['_id'],
                        brand                = products_list[p]['brand'],
                        colorway             = products_list[p]['colorway'],                    
                        gender               = products_list[p]['gender'],
                        description          = products_list[p]['story'],
                        name                 = products_list[p]['name'],
                        releaseDate          = products_list[p]['releaseDate'],
                        retailPrice          = products_list[p]['retailPrice'],
                        estimatedMarketValue = products_list[p]['estimatedMarketValue'],
                        sku                  = products_list[p]['sku'],
                        imageUrl             = products_list[p]['image']['original'],
                        smallImageUrl        = products_list[p]['image']['small'],
                        thumbUrl             = products_list[p]['image']['thumbnail'],
                )
            kick.save()
        # create_new_kick_data(products_list, p)

    return HttpResponse(status= status.HTTP_201_CREATED)