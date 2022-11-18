from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from .models import kicks
import pprint
import requests
import json

'''
StockX Data paser v1.0.0

'''
pp = pprint.PrettyPrinter(indent=4)
def stockX_data_paser(request, query):
    
    # query2= 'jordan 1'
    
    url = f'https://stockx.com/api/browse?_search={query}&page=1'
    
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

    response = requests.get(url=url, headers=headers)
    json_data = json.loads(response.text)
    products_list = json_data['Products']    
    
    for p in range(len(products_list)):
        try:
            kicks.objects.get(uuid=products_list[p]['uuid'])
            print('Already exists')
        except kicks.DoesNotExist:
            print('No RESULT')

    # pp.pprint( products_list[0]['uuid'])
    # pp.pprint(products_list[0])
    
    return HttpResponse(json_data['Products'][0])