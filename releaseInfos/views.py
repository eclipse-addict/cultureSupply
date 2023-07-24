import requests
import json
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from pprint import pprint as print
from bs4 import BeautifulSoup
from .models import ReleaseInfo
from products.models import kicks
from .serializers import ReleaseInfoSerializer
def get_ongoing_release_detail(request, prd_sku):
    '''
    요청 시점 : 페이지 로드 후 monuted 됐을 때, 요청 후 count 값 확인.
    이전 count 값과 다르면, 새로운 release가 있음을 확인 후,
    새로운 release가 있으면, 해당 release를 DB에 저장하고,
    새로운 release가 없으면, DB에 저장된 release를 가져온다.
    '''

    product = kicks.objects.get(sku=prd_sku)

    BASE_URL = 'https://www.shoeprize.com/'
    url = BASE_URL + f'api/v2/search/?q={prd_sku}'

    response = requests.get(url).json() # sku로 검색한 결과
    result_counts = int(requests.get(url).json().get('products').get('count'))
    print(f'result_counts : {result_counts}')
    if result_counts:  # 검색 결과가 있을 때
        for i in range(0, result_counts):   # 검색 결과의 개수만큼 반복
            prd_id = response.get('products').get('results')[i].get('id')  # 검색 결과에서 제품 id 추출
            print(f'prd_id : {prd_id}')
            # 검색 결과에서 제품 id로 상품 세부 검색
            release_data_res = requests.get(BASE_URL + f'api/v2/releases/?page=1&product_id={prd_id}&page_size=50&is_end=false&ordering=end_time,-id')   # 검색 결과에서 제품 id로 상품 세부 검색 및 종료되지 않은 release만 가져옴
            # print(f'request url : {BASE_URL + f"api/v2/releases/?page=1&product_id={prd_id}&page_size=50&is_end=false&ordering=end_time,-id"}')
            results = release_data_res.json().get('results')
            print(f'results : {release_data_res.json()}')
            release_data_check_list = ReleaseInfo.objects.filter(product=product)
            ids = []
            for _ in release_data_check_list:
                ids.append(_.platform_pk)


                # print('새로운 release가 있음')
            for r in results:
                # print(f"r.get('product').get('code') : {r.get('product').get('code')}")
                if prd_sku == r.get('product').get('code'):  # 검색 결과의 sku와 요청한 sku가 같을 때
                    if r.get('id') not in ids:
                        release_data = ReleaseInfo.objects.create(
                            platform_pk=r.get('id'),
                            announced_date=r.get('announcedTimestamp'),
                            end_time_date=r.get('endTimestamp'),
                            date_info=r.get('dateInfo'),
                            isDomestic=r.get('isDomesticSite'),
                            isExpired=r.get('isExpired'),
                            announcement_method=r.get('method'),
                            payment_method=r.get('payMethod'),
                            sale_price=r.get('salePrice'),
                            sale_price_currency=r.get('salePriceCurrency'),
                            currencySymbol=r.get('salePriceCurrencySymbol'),
                            region=r.get('region'),
                            product=product,
                            raffle_url=r.get('url'),
                            site_name=r.get('releaseMarket').get('name'),
                            shipping_method=r.get('shippingMethod')
                        )
        release_data = ReleaseInfo.objects.filter(product=product).order_by('-announced_date')
        print(f'release_data : {release_data}')
        serializer = ReleaseInfoSerializer(release_data, many=True)
        json_data = json.dumps(serializer.data, ensure_ascii=False)
    return JsonResponse(data=serializer.data, status=status.HTTP_200_OK, safe=False)


def get_kream_price_Info(reqeust, prd_sku):
    url = f'https://kream.co.kr/api/p/tabs/all/?keyword={prd_sku}&request_key=1175edd6-81b3-4bce-8568-664d0c574152'
    headers = {
        "Authority": "kream.co.kr",
        "Method": "GET",
        "Path": "/api/p/tabs/all/?keyword=CZ0790-106&request_key=1175edd6-81b3-4bce-8568-664d0c574152",
        "Scheme": "https",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "i18n_redirected=kr; ab.storage.sessionId.8d5d348c-fc26-4528-a5b4-627447ffad5a=%7B%22g%22%3A%2272df04b7-7c15-0603-6997-d0ce52a6208e%22%2C%22e%22%3A1685407802682%2C%22c%22%3A1685406002682%2C%22l%22%3A1685406002682%7D; ab.storage.deviceId.8d5d348c-fc26-4528-a5b4-627447ffad5a=%7B%22g%22%3A%228c6af36e-10e1-e99c-feda-4ec4ccfa4845%22%2C%22c%22%3A1685406002683%2C%22l%22%3A1685406002683%7D; _fbp=fb.2.1685406002693.67349702; afUserId=ad7f55e6-bd93-4c32-84f2-534b191bb1c2-p; strategy=local; did=a15eb7e5-0713-4cf8-a253-94cc20a9faae; AF_SYNC=1689599100861; _gid=GA1.3.1882520390.1689991537; AMP_MKTG_487619ef1d=JTdCJTdE; wcs_bt=s_59a6a417df3:1689991865; _ga_SRFKTMTR0R=GS1.1.1689991536.6.1.1689991865.59.0.0; _ga_5LYDPM15LW=GS1.1.1689991536.4.1.1689991865.59.0.0; _ga=GA1.3.1971266654.1685406003; _gat_gtag_UA_153398119_1=1; AMP_487619ef1d=JTdCJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJkZXZpY2VJZCUyMiUzQSUyMmQxYWZmYWZmLTY4OTMtNGM0MC1iMzQ1LTM3MGI3ZDE3YzZlMCUyMiUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNjg5OTkxODc0MDk0JTJDJTIyc2Vzc2lvbklkJTIyJTNBMTY4OTk5MTUzNjExMiU3RA==",
        "Referer": "https://kream.co.kr/",
        "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Kream-Api-Version": "20",
        "X-Kream-Client-Datetime": "20230722111114+0900",
        "X-Kream-Device-Id": "web;a15eb7e5-0713-4cf8-a253-94cc20a9faae"
    }
    response = requests.get(url, headers=headers).json()
    if response.get("items"):
        original_price = response.get("items")[0].get('product').get("release").get("original_price")
        # print(response.get("items")[0].get('product').get("release").get("original_price"))
        market_price =  response.get("items")[0].get('product').get('market').get('market_price')
        price_premium =  response.get("items")[0].get('product').get('market').get('pricepremium')
        pricepremium_percentage =  response.get("items")[0].get('product').get('market').get('pricepremium_percentage')
        result = {
            'original_price': original_price,
            'market_price': market_price,
            'price_premium': price_premium,
            'pricepremium_percentage': pricepremium_percentage
        }
        return JsonResponse(data={'result': result}, status=status.HTTP_200_OK)
    return JsonResponse(data={'result': 'no data'}, status=status.HTTP_200_OK)
