import datetime
import json
import os
import pprint
import time
import urllib.request as req
from urllib.parse import urlparse

import chardet
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from google_images_download import google_images_download
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from assets.brand_list import brand_list
from ..models import kicks, productImg, ProductCrawlingFlag

User = get_user_model()

"""
sneakers Data paser v1.0.0

"""
pp = pprint.PrettyPrinter(indent=4)
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "utf-8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Origin": "https://thesneakerdatabase.com",
    "app-platform": "Iron",
    # 'Host': '',
    "referer": "https://thesneakerdatabase.com/sneakers/6778a67b-669c-4c3e-8ca0-2d3f1c911a8b",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}
goat_headers = {
    "accept": "*/*",
    "accept-encoding": "utf-8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Origin": "https://www.goat.com",
    "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}

new_release_url = getattr(settings, "NEW_RELEASE_URL", None)


#  카테고리 별 제품 파싱 :
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
                f"https://ac.cnstrc.com/browse/group_id/all?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=11&page={i}&num_results_per_page=200&filters[recently_released]=sneakers&sort_by=release_date&sort_order=descending&fmt_options[hidden_fields]=gp_lowest_price_cents_3&fmt_options[hidden_fields]=gp_instant_ship_lowest_price_cents_3&fmt_options[hidden_facets]=gp_lowest_price_cents_3&fmt_options[hidden_facets]=gp_instant_ship_lowest_price_cents_3&_dt=1670822296441",
                f"https://ac.cnstrc.com/browse/group_id/all?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=11&page={i}&num_results_per_page=200&filters[recently_released]=apparel&sort_by=date_added&sort_order=descending&fmt_options[hidden_fields]=gp_lowest_price_cents_3&fmt_options[hidden_fields]=gp_instant_ship_lowest_price_cents_3&fmt_options[hidden_facets]=gp_lowest_price_cents_3&fmt_options[hidden_facets]=gp_instant_ship_lowest_price_cents_3&_dt=1670822445157",
                f"https://ac.cnstrc.com/browse/collection_id/new-arrivals-apparel?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=12&page={i}&num_results_per_page=200&filters%5Bproduct_condition%5D=new_no_defects&sort_by=relevance&sort_order=descending&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670910536899",
                f"https://ac.cnstrc.com/browse/collection_id/just-dropped?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=12&page={i}&num_results_per_page=200&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670910906505",
                f"https://ac.cnstrc.com/browse/collection_id/women-s-sneakers?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=12&page={i}&num_results_per_page=200&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670910951588",
                f"https://ac.cnstrc.com/browse/collection_id/toddler?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=12&page={i}&num_results_per_page=200&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670910987178",
                f"https://ac.cnstrc.com/browse/collection_id/most-wanted-new?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=12&page={i}&num_results_per_page=200&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670911039677",
            ]

            url_list_name = [
                "popular_release",
                "recent_kicks",
                "recent_apparel",
                "newe_in",
                "just_drop",
                "womens",
                "toddler",
                "most_wanted",
            ]

            response = requests.get(url=url_list[j], headers=goat_headers)
            json_data = json.loads(response.text)
            products_list = json_data.get("response").get("results")

            if not products_list:
                break

            for p in range(len(products_list)):
                brand = products_list[p]["data"].get("brand")
                new_cnt += create_new_kick_data(products_list, p, brand)

    last_updated_flag = ProductCrawlingFlag(updated_item_cnt=new_cnt)
    last_updated_flag.save()

    return JsonResponse(
        {"new_product_count": new_cnt, "time": time.time() - start},
        status=status.HTTP_201_CREATED,
    )


# 284,361 /200 = // current 21 page
def get_goat(request):
    new_cnt = 0
    for brand in brand_list:  # brand 먼저 픽스
        for i in range(1, 300):
            all_year_by_brand_url = f"https://ac.cnstrc.com/browse/group_id/all?c=ciojs-client-2.29.12&key=key_XT7bjdbvjgECO5d8&i=6af107e4-772b-4fae-bff6-510ed4c70068&s=9&page={i}&num_results_per_page=200&filters%5Brelease_date_year%5D=2022&filters%5Brelease_date_year%5D=2021&filters%5Brelease_date_year%5D=2020&filters%5Brelease_date_year%5D=2018&filters%5Brelease_date_year%5D=2019&filters%5Brelease_date_year%5D=2017&filters%5Brelease_date_year%5D=2016&filters%5Brelease_date_year%5D=2023&filters%5Brelease_date_year%5D=2015&filters%5Brelease_date_year%5D=2014&filters%5Brelease_date_year%5D=2013&filters%5Brelease_date_year%5D=2012&filters%5Brelease_date_year%5D=2011&filters%5Brelease_date_year%5D=2010&filters%5Brelease_date_year%5D=2008&filters%5Brelease_date_year%5D=2009&filters%5Brelease_date_year%5D=2006&filters%5Brelease_date_year%5D=2007&filters%5Brelease_date_year%5D=2005&filters%5Brelease_date_year%5D=2004&filters%5Brelease_date_year%5D=2002&filters%5Brelease_date_year%5D=2003&filters%5Brelease_date_year%5D=2001&filters%5Brelease_date_year%5D=2000&filters%5Brelease_date_year%5D=1999&filters%5Brelease_date_year%5D=1998&filters%5Brelease_date_year%5D=1997&filters%5Brelease_date_year%5D=1996&filters%5Brelease_date_year%5D=1985&filters%5Brelease_date_year%5D=1986&filters%5Brelease_date_year%5D=1989&filters%5Brelease_date_year%5D=1991&filters%5Brelease_date_year%5D=1993&filters%5Brelease_date_year%5D=1995&filters%5Brelease_date_year%5D=1994&filters%5Brelease_date_year%5D=1992&filters%5Brelease_date_year%5D=1990&filters%5Brelease_date_year%5D=1988&filters%5Bbrand%5D={brand.lower()}&sort_by=gp_lowest_price_cents_3&sort_order=ascending&fmt_options%5Bhidden_fields%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_fields%5D=gp_instant_ship_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_lowest_price_cents_3&fmt_options%5Bhidden_facets%5D=gp_instant_ship_lowest_price_cents_3&_dt=1670814405023"

            response = requests.get(url=all_year_by_brand_url, headers=goat_headers)
            json_data = json.loads(response.text)
            products_list = json_data.get("response").get("results")

            if not products_list:
                break

            for p in range(len(products_list)):
                new_cnt += create_new_kick_data(products_list, p, brand)

    return HttpResponse(status=status.HTTP_201_CREATED)


def get_info_from_sku(prd_sku):
    kream_headers = {
        "Authority": "kream.co.kr",
        "Method": "GET",
        "Path": "/api/p/tabs/all/?keyword=CZ0790-106&request_key=1175edd6-81b3-4bce-8568-664d0c574152",
        "Scheme": "https",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "i18n_redirected=kr; ab.storage.sessionId.8d5d348c-fc26-4528-a5b4-627447ffad5a=%7B%22g%22%3A%2272df04b7-7c15-0603-6997-d0ce52a6208e%22%2C%22e%22%3A1685407802682%2C%22c%22%3A1685406002682%2C%22l%22%3A1685406002682%7D; ab.storage.deviceId.8d5d348c-fc26-4528-a5b4-627447ffad5a=%7B%22g%22%3A%228c6af36e-10e1-e99c-feda-4ec4ccfa4845%22%2C%22c%22%3A1685406002683%2C%22l%22%3A1685406002683%7D; _fbp=fb.2.1685406002693.67349702; afUserId=ad7f55e6-bd93-4c32-84f2-534b191bb1c2-p; strategy=local; did=a15eb7e5-0713-4cf8-a253-94cc20a9faae; AF_SYNC=1689599100861; _gid=GA1.3.1882520390.1689991537; AMP_MKTG_487619ef1d=JTdCJTdE; wcs_bt=s_59a6a417df3:1689991865; _ga_SRFKTMTR0R=GS1.1.1689991536.6.1.1689991865.59.0.0; _ga_5LYDPM15LW=GS1.1.1689991536.4.1.1689991865.59.0.0; _ga=GA1.3.1971266654.1685406003; _gat_gtag_UA_153398119_1=1; AMP_487619ef1d=JTdCJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJkZXZpY2VJZCUyMiUzQSUyMmQxYWZmYWZmLTY4OTMtNGM0MC1iMzQ1LTM3MGI3ZDE3YzZlMCUyMiUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNjg5OTkxODc0MDk0JTJDJTIyc2Vzc2lvbklkJTIyJTNBMTY4OTk5MTUzNjExMiU3RA==",
        "Referer": "https://kream.co.kr/",
        "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Kream-Api-Version": "20",
        "X-Kream-Client-Datetime": "20230722111114+0900",
        "X-Kream-Device-Id": "web;a15eb7e5-0713-4cf8-a253-94cc20a9faae",
    }

    url = f"https://kream.co.kr/api/p/tabs/all/?keyword={prd_sku}&request_key=1175edd6-81b3-4bce-8568-664d0c574152"

    response = requests.get(url, headers=kream_headers).json()

    if response.get("items"):
        retail_price_krw = 0
        category = (
            response.get("items")[0].get("product").get("release").get("category")
        )
        translated_name = (
            response.get("items")[0]
            .get("product")
            .get("release")
            .get("translated_name")
        )
        colorway = (
            response.get("items")[0].get("product").get("release").get("colorway")
        )
        brand = response.get("items")[0].get("product").get("brand").get("name")
        released_data = (
            response.get("items")[0].get("product").get("release").get("date_released")
        )
        image_url = (
            response.get("items")[0].get("product").get("release").get("image_urls")[0]
        )  # error
        gender = response.get("items")[0].get("product").get("release").get("gender")
        currency = (
            response.get("items")[0]
            .get("product")
            .get("release")
            .get("original_price_currency")
        )

        if currency == "KRW":
            retail_price_krw = (
                response.get("items")[0]
                .get("product")
                .get("release")
                .get("original_price")
            )

        result = {
            "category": category,
            "translated_name": translated_name,
            "colorway": colorway,
            "brand": brand,
            "released_data": released_data,
            "image_url": image_url,
            "gender": gender,
            "retail_price_krw": retail_price_krw,
        }
        return result
    return None


def create_new_kick_data(products_list, p, brand):
    print(f"products_list[p]['value']: {brand} {products_list[p].get('value')}")
    try:
        if not products_list[p]["data"].get("sku"):
            print(f'No sku found for {products_list[p].get("name")}')
            return 0

        else:
            sku = products_list[p]["data"].get("sku")
            new_sku = str(sku).replace(" ", "-")
            kick = kicks.objects.get(sku=new_sku)

            result = 0
            sku_result = get_info_from_sku(new_sku)
            if sku_result:
                # "기존 제품 sku 를 통해 kream 에서 정보 가져오기 성공."
                if not kick.category:
                    kick.category = sku_result.get("category")
                    result = 1

                if not kick.name_kr:
                    kick.name = sku_result.get("translated_name")
                    result = 1

                if not kick.retailPrice:
                    kick.retailPrice = sku_result.get("original_price")
                    result = 1

                if not kick.colorway:
                    kick.colorway = sku_result.get("colorway")
                    result = 1

                if not kick.brand:
                    kick.brand = sku_result.get("brand")
                    result = 1

                if not kick.retail_price_krw:
                    kick.retail_price_krw = sku_result.get("retail_price_krw")
                    result = 1

                if not kick.releaseDate:
                    if sku_result.get("released_data"):  # kream 에서 가져온 출시일이 있으면
                        #   change format of data  from '2023-07-29T00:00:00Z' to '2023-07-29'
                        kream_date = "2023-07-29T00:00:00Z"  # Example input date, replace this with the actual kream date
                        kream_date = datetime.strptime(
                            kream_date, "%Y-%m-%dT%H:%M:%SZ"
                        )  # Parse the input date string
                        formatted_kream_date = kream_date.strftime(
                            "%Y-%m-%d"
                        )  # Format the date to YYYY-MM-DD
                        release_date = formatted_kream_date  # Assign the formatted date to releaseDate

                if (
                    kick.local_imageUrl == "media/images/defaultImg.png"
                    and sku_result.get("image_url")
                ):
                    imageUrl = sku_result.get("image_url")

                    file_name = os.path.basename(imageUrl)
                    path = urlparse(imageUrl).path
                    path_url = path[: path.find(file_name)]

                    try:
                        req.urlretrieve(
                            imageUrl,
                            "/var/services/web/kickin/media/images/sneakers/"
                            + file_name,
                        )  # 경로에 해당 제품 이미지 저장
                        # 해당 제품 db 업데이트
                        img_url = "media/images/sneakers/" + file_name  # db에 저장할 경로
                        kick.local_imageUrl = img_url
                        result = 1
                    except:  # 이미지 다운로드 실패시
                        print(f"!!!이미지 다운로드 Error occured!!!")
                if not kick.gender:
                    kick.gender = sku_result.get("gender")
                    result = 1

            if result > 0:  # 변경사항이 있으면 저장
                kick.save()
                return 1  # 변경사항이 있으면 1 리턴

            return 0  # 변경사항이 없으면 0 리턴

    except kicks.DoesNotExist:  # 존재하지 않는 제품이므로, 등록 처리
        sku = products_list[p]["data"].get("sku")
        new_sku = str(sku).replace(" ", "-")  # sku에 공백이 있으면 -로 변경
        date_format = "%Y%m%d"  # date format
        kream_result = get_info_from_sku(new_sku)  # sku로 제품 정보 가져오기
        (
            kream_category,
            kream_translated_name,
            kream_retail_price_krw,
            kream_colorway,
            kream_brand,
            kream_released_data,
            kream_image_url,
            kream_gender,
        ) = (None, None, None, None, None, None, None, None)
        if kream_result:  # 제품 정보가 있으면
            kream_category = kream_result.get("category")  # 카테고리
            kream_translated_name = kream_result.get("translated_name")  # 한글 제품명
            kream_retail_price_krw = kream_result.get("retail_price_krw")  # 정가
            kream_colorway = kream_result.get("colorway")  # 컬러웨이
            kream_brand = kream_result.get("brand")  # 브랜드
            released_data = kream_result.get("released_data")  # 출시일
            image_url = kream_result.get("image_url")  # 이미지 url
            gender = kream_result.get("gender")  # 성별

        release_date = products_list[p]["data"].get("release_date")
        # if releaseDate is not null format the date to YYYY-MM-DD
        if release_date:  # releaseDate 가 null 이 아니면
            release_date = str(release_date).strip("()").strip(",")  # () , 제거
            release_date = datetime.datetime.strptime(
                str(release_date), date_format
            )  # date format 변경
            release_date = str(release_date.date())
        elif kream_released_data:  # kream 에서 가져온 출시일이 있으면
            #   change format of data  from '2023-07-29T00:00:00Z' to '2023-07-29'
            kream_date = "2023-07-29T00:00:00Z"  # Example input date, replace this with the actual kream date
            kream_date = datetime.strptime(
                kream_date, "%Y-%m-%dT%H:%M:%SZ"
            )  # Parse the input date string
            formatted_kream_date = kream_date.strftime(
                "%Y-%m-%d"
            )  # Format the date to YYYY-MM-DD
            release_date = (
                formatted_kream_date  # Assign the formatted date to releaseDate
            )

        kick = kicks(
            uuid=products_list[p]["data"].get("id"),
            name=products_list[p].get("value"),
            name_kr=kream_translated_name,
            brand=kream_brand if kream_brand else brand,
            category=kream_category
            if kream_category
            else products_list[p]["data"].get("category"),
            product_type=products_list[p]["data"].get("product_type"),
            colorway=kream_colorway
            if kream_colorway
            else products_list[p]["data"].get("color"),
            releaseDate=release_date,
            release_date_year=products_list[p]["data"].get("release_date_year"),
            retailPrice=products_list[p]["data"].get("retail_price_cents"),
            retail_price_krw=kream_retail_price_krw,
            sku=new_sku,
            imageUrl=products_list[p]["data"].get("image_url"),
            slug=products_list[p]["data"].get("slug"),
            gender=kream_gender if kream_gender else "",
        )
        kick.save()

        if (
            kick.imageUrl and kick.imageUrl.find("stockx") == -1
        ):  # kick.imageUrl is not null and not stockx image
            imageUrl = kick.imageUrl  # kick.imageUrl 담아놓고

            # 저장 경로
            file_name = os.path.basename(imageUrl)
            path = urlparse(imageUrl).path
            path_url = path[: path.find(file_name)]

            # 설정한 경로에 파일 저장
            try:
                # /var/services/web/kickin/media/images/sneakers/ -> server_path
                # /Users/isaac/Desktop/Project/culturesupply/media/images/sneakers/ -> local_path
                req.urlretrieve(
                    imageUrl,
                    "/var/services/web/kickin/media/images/sneakers/" + file_name,
                )  # 경로에 해당 제품 이미지 저장
                # 해당 제품 db 업데이트
                img_url = "media/images/sneakers/" + file_name  # db에 저장할 경로
                kick.local_imageUrl = img_url  # db에 저장할 경로 담아놓고
                kick.save()  # db에 저장

            except:  # 이미지 다운로드 실패시
                print(f"Error occured")
                if kream_image_url:
                    print(f"URL Check(kream_image_url):{kick.imageUrl}")
                    kick.imageUrl = kream_image_url
                    file_name = os.path.basename(imageUrl)
                    path = urlparse(imageUrl).path
                    path_url = path[: path.find(file_name)]
                    try:
                        # /var/services/web/kickin/media/images/sneakers/ -> server_path
                        # /Users/isaac/Desktop/Project/culturesupply/media/images/sneakers/ -> local_path
                        req.urlretrieve(
                            imageUrl,
                            "/var/services/web/kickin/media/images/sneakers/"
                            + file_name,
                        )  # 경로에 해당 제품 이미지 저장
                        # 해당 제품 db 업데이트
                        img_url = "media/images/sneakers/" + file_name  # db에 저장할 경로
                        kick.local_imageUrl = img_url  # db에 저장할 경로 담아놓고
                        kick.save()  # db에 저장

                    except:  # 이미지 다운로드 실패시
                        kick.imageUrl = "media/images/defaultImg.png"  # 기본 이미지로 저장
                        kick.save()  # db에 저장

        return 1  # 신제품 등록 처리 완료


def save_product_img(products_list, p, kick):
    img_type_list = ["left", "back", "top", "bottom", "additional"]
    img_url = products_list[p]["data"].get("image_url")
    if img_url:
        img = productImg(product=kick, img_url=img_url, type="right")
    else:
        img = productImg(
            product=kick,
            img_url="http://localhost:8000/media/images/defaultImg.png",
            type="right",
        )
    img.save()

    for type in img_type_list:
        img = productImg(
            product=kick,
            img_url="http://localhost:8000/media/images/defaultImg.png",
            type=type,
        )
        img.save()


def new_release_paser(request):
    response = requests.get(url=new_release_url, headers=headers)
    print(response.status_code)

    new_cnt = 0
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        data = soup.select_one("#__NEXT_DATA__").get_text()
        json_data = json.loads(data)
        products_list = json_data["props"]["pageProps"]["newReleases"]

    for p in range(len(products_list)):
        new_cnt += create_new_kick_data(products_list, p)
    print(f"new Count = {new_cnt}")
    return HttpResponse(status=status.HTTP_201_CREATED)
    # return JsonResponse(json_data['props']['pageProps']['newReleases'], safe=False)


def data_by_year_paser_by_brand_paser(request):
    response = requests.get(url=new_release_url, headers=headers)
    json_data = json.loads(response.text)
    products_list = json_data["data"]

    for p in range(len(products_list)):
        create_new_kick_data(products_list, p)

    return HttpResponse(status=status.HTTP_201_CREATED)


def sneaker_data_by_brand_paser(request):
    j_url_m = getattr(settings, "J_URL_M", None)
    j_url_f = getattr(settings, "J_URL_F", None)
    n_url_m = getattr(settings, "N_URL_M", None)
    n_url_f = getattr(settings, "N_URL_M", None)

    cnt = 0
    response = requests.get(url=n_url_f, headers=headers)
    json_data = json.loads(response.text)
    products_list = json_data["data"]

    for p in range(len(products_list)):
        cnt += create_new_kick_data(products_list, p)

    print(f"new Count : {cnt}")

    return HttpResponse(status=status.HTTP_201_CREATED)


def sneaker_img_paser(request):
    start = time.time()
    count = 0
    # 이미 추가한 것 필터로 빼고 갖고오기..
    all_products = (
        kicks.objects.filter(local_imageUrl="media/images/defaultImg.png")
        .exclude(imageUrl__isnull=True)
        .order_by("-releaseDate")
    )

    for i, p in enumerate(all_products):
        if p.imageUrl != "" and p.imageUrl.find("stockx") == -1:
            imageUrl = p.imageUrl
            # 저장 경로
            file_name = os.path.basename(imageUrl)
            path = urlparse(imageUrl).path
            path_url = path[: path.find(file_name)]

            try:
                req.urlretrieve(
                    imageUrl,
                    "/var/services/web/kickin/media/images/sneakers/" + file_name,
                )
                # 해당 제품 db 업데이트
                img_url = "media/images/sneakers/" + file_name
                p.local_imageUrl = img_url
                p.save()
                count += 1

            except:
                print(f"Error occured")
                p.imageUrl = "media/images/defaultImg.png"
                p.save()

        # Stockx url 일 경우,
        elif p.imageUrl != "" and p.imageUrl.find("stockx") >= 0:
            print(f"Name check (stockX) : {p.name}")
            opener = req.build_opener()
            opener.addheaders = [
                (
                    "User-Agent",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36",
                )
            ]

            req.install_opener(opener)
            print(f"encode : {chardet.detect(p.imageUrl.encode())}")
            imageUrl = p.imageUrl

            file_name = os.path.basename(imageUrl)
            path = urlparse(imageUrl).path
            path_url = path[: path.find(file_name)]
            # 저장 경로
            local_path = (
                "/Users/isaac/Desktop/Project/culturesupply/media/images/sneakers"
                + path
            )
            # 저장 할 제품 이름
            file_name = os.path.basename(imageUrl)
            try:
                req.urlretrieve(
                    imageUrl,
                    "/var/services/web/kickin/media/images/sneakers/"
                    + file_name[: file_name.find("?")],
                )
                # 해당 제품 db 업데이트
                img_url = "media/images/sneakers/" + file_name[: file_name.find("?")]
                p.local_imageUrl = img_url
                p.save()

                img = productImg.objects.filter(product=p).filter(type="right")
                img.img_url = img_url
                img.save()
                count += 1
            except:
                print(f"Error occured")
                p.imageUrl = "media/images/defaultImg.png"
                p.save()

                img = productImg.objects.filter(product=p).filter(type="right")
                img.img_url = "media/images/defaultImg.png"
                img.save()

    print(f"{time.time() - start}")
    return HttpResponse(status=status.HTTP_200_OK)


def check_dir(local_path):
    try:
        if not os.path.exists(local_path):
            os.makedirs(local_path)
    except OSError:
        print(OSError.strerror)


def google_img_download(request):
    all_products = kicks.objects.filter(imageUrl="").order_by("-releaseDate")

    for p in all_products:
        response = google_images_download.googleimagesdownload()  # class instantiation
        arguments = {
            "keywords": p.name,
            "limit": 1,
            "print_urls": True,
            "image_directory": "images/sneakers/",
            "output_directory": "media/",
        }

        try:
            paths = response.download(arguments)

            raw_url = paths[0][list(paths[0].keys())[0]]

            print(
                f'final check2 : {"http://localhost:8000" + raw_url[0][raw_url[0].find("/media"):]}'
            )  #
            p.local_imageUrl = (
                "http://localhost:8000" + raw_url[0][raw_url[0].find("/media") :]
            )
            p.save()

        except Exception as error:
            print(f"error : {error}")
            continue

    return HttpResponse(status.HTTP_201_CREATED)


def duplicate_check(request):
    all_products = (
        kicks.objects.all().exclude(sku__isnull=True).order_by("-releaseDate")
    )
    for p in all_products:
        sku = p.sku
        if not sku:
            print(f"sku is NULL")
        else:
            if sku.find("-") != -1:
                print(f'sku check "-" 있음: {sku}, {p.name}')
                new_sku = sku.replace("-", " ")  # 하이픈 없앤 형태로 중복 체크
                # print(f'sku "-".strip : {new_sku}')
                duplicate = kicks.objects.filter(sku=new_sku)
                if duplicate:
                    print(f"sku duplicate : {duplicate[0].sku}")
                    print(f"sku duplicate : {duplicate[0].name}")
                    duplicate.delete()

    return HttpResponse(status.HTTP_200_OK)


"""
기존 이미지 -> 이미지 테이블에 저장. 
"""


def select_all_and_add_img_model(request):
    img_type_list = [
        "right",
        "left",
        "back",
        "top",
        "bottom",
        "additional",
    ]  # 이미지 타입 리스트
    # all_products = kicks.objects.all()
    # 나누자.. 디폴트 이미지와 아닌것 두번으로 QuerySet 나누기
    product_count = kicks.objects.all().count()
    chunk_size = 1000
    # all_products = kicks.objects.filter(Q(local_imageUrl__icontains='media/images/defaultImg.png'))
    for i in range(0, product_count, chunk_size):
        print(f"count : {i} ~ {i + chunk_size}")
        all_products = kicks.objects.all()[i : i + chunk_size]

        for p in all_products:
            if p.local_imageUrl != "media/images/defaultImg.png":  # 기존 이미지가 존재 하는 경우
                img = productImg(
                    product=p,
                    img_url=p.local_imageUrl,
                    type="right",  # right 이미지만 제품 이미지로 저장
                )
                img.save()

                for type in img_type_list:
                    if type == "right":  # right 이미지는 이미 저장했으므로
                        continue

                    img = productImg(  # left, back, top, bottom, additional 이미지 저장
                        product=p, img_url="media/images/defaultImg.png", type=type
                    )
                    img.save()

            else:  # 기본 이미지 없는 경우 타입 리스트 순회하며, 기본 이미지 저장
                for type in img_type_list:
                    img = productImg(
                        product=p, img_url="media/images/defaultImg.png", type=type
                    )
                    img.save()

    return HttpResponse(status.HTTP_200_OK)


def temp_img_fix(request):
    right_img_list = productImg.objects.filter(type="right").filter(
        Q(img_url__icontains="https://image.goat.com/")
    )

    for img in right_img_list:
        product = kicks.objects.get(id=img.product.id)
        if (
            product.local_imageUrl
            != "http://localhost:8000/media/images/defaultImg.png"
        ):
            img.img_url = product.local_imageUrl
            img.save()

    return HttpResponse(status.HTTP_200_OK)


def img_url_updator(reqeust):
    print("img_url_updator")
    products = productImg.objects.all()
    print("products size : ", len(products))

    for i, p in enumerate(products):
        print(f"p : {p.img_url}")
        p.img_url = p.img_url.replace("http://localhost:8000/", "")
        print(f"p : {p.img_url}")
        p.save()

    res = HttpResponse("success" + str(len(products)))
    res.status_code = 200

    return res


@api_view(["GET"])
@permission_classes([AllowAny])
def kream_crawling(request):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "i18n_redirected=kr; ab.storage.sessionId.8d5d348c-fc26-4528-a5b4-627447ffad5a=%7B%22g%22%3A%2272df04b7-7c15-0603-6997-d0ce52a6208e%22%2C%22e%22%3A1685407802682%2C%22c%22%3A1685406002682%2C%22l%22%3A1685406002682%7D; ab.storage.deviceId.8d5d348c-fc26-4528-a5b4-627447ffad5a=%7B%22g%22%3A%228c6af36e-10e1-e99c-feda-4ec4ccfa4845%22%2C%22c%22%3A1685406002683%2C%22l%22%3A1685406002683%7D; _fbp=fb.2.1685406002693.67349702; afUserId=ad7f55e6-bd93-4c32-84f2-534b191bb1c2-p; did=a15eb7e5-0713-4cf8-a253-94cc20a9faae; _token.local=false; _refresh_token.local=false; strategy=local; AF_SYNC=1690270813981; _gid=GA1.3.1007280691.1690377081; AMP_MKTG_487619ef1d=JTdCJTdE; AMP_487619ef1d=JTdCJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJkZXZpY2VJZCUyMiUzQSUyMmQxYWZmYWZmLTY4OTMtNGM0MC1iMzQ1LTM3MGI3ZDE3YzZlMCUyMiUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNjkwMzc5ODE5OTQ0JTJDJTIyc2Vzc2lvbklkJTIyJTNBMTY5MDM3OTcyNjEzMSU3RA==; wcs_bt=s_59a6a417df3:1690380790; _ga_SRFKTMTR0R=GS1.1.1690379727.18.1.1690380790.60.0.0; _ga_5LYDPM15LW=GS1.1.1690379727.16.1.1690380791.59.0.0; _ga=GA1.3.1971266654.1685406003; _gat_gtag_UA_153398119_1=1",
        "Referer": "https://kream.co.kr/search?keyword=698696-100",
        "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-Kream-Api-Version": "20",
        "X-Kream-Client-Datetime": "20230726231317+0900",
        "X-Kream-Device-Id": "web;a15eb7e5-0713-4cf8-a253-94cc20a9faae",
    }
    # products = kicks.objects.filter(Q(local_imageUrl__icontains='media/images/defaultImg.png')|
    #                                 Q(name_kr='')|Q(name_kr__isnull=True)| Q(brand='')|Q(brand__isnull=True)|
    #                                 Q(category='')|Q(category__isnull=True))
    products = kicks.objects.all()

    for p in products:
        url = f"https://kream.co.kr/api/p/tabs/all/?keyword={p.sku}&request_key=1175edd6-81b3-4bce-8568-664d0c574152"
        response = requests.get(url, headers=headers).json()

        if response.get("items"):
            if not p.name_kr:
                translated_name = (
                    response.get("items")[0]
                    .get("product")
                    .get("release")
                    .get("translated_name")
                )
                p.name_kr = translated_name

            if not p.brand:
                brand = response.get("items")[0].get("product").get("brand").get("name")
                p.brand = brand

            if not p.category:
                category = (
                    response.get("items")[0]
                    .get("product")
                    .get("release")
                    .get("category")
                )
                p.category = category

            local_price_currency = (
                response.get("items")[0]
                .get("product")
                .get("release")
                .get("local_price_currency")
            )
            original_price = (
                response.get("items")[0]
                .get("product")
                .get("release")
                .get("original_price")
            )

            if local_price_currency == "KRW" and original_price:
                p.retail_price_krw = original_price
            colorway = (
                response.get("items")[0].get("product").get("release").get("colorway")
            )

            if not p.colorway:
                p.colorway = colorway
            p.save()

    return HttpResponse(status.HTTP_200_OK)
