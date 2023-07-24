from django.db import models
# Create your models here.
class ReleaseInfo(models.Model):
    platform_pk = models.BigIntegerField(null=True, blank=True)
    announced_date = models.DateTimeField(auto_now_add=True)
    end_time_date = models.DateTimeField(auto_now_add=True)
    date_info = models.CharField(max_length=150)  # "7월 22일 (토) 09:00 ~ 7월 27일 (목) 08:59"
    isDomestic = models.BooleanField(default=True)  # 라플의 국내 여부
    isExpired = models.BooleanField(default=False)  # 라플의 기간이 지났는지 여부
    announcement_method = models.CharField(max_length=150)  # 라플의 공지 방식
    payment_method = models.CharField(max_length=150)  # 라플의 결제 방식
    sale_price = models.CharField(max_length=150)  # 제품 가격
    sale_price_currency = models.CharField(max_length=150)  # 제품 가격의 통화
    currencySymbol = models.CharField(max_length=150)  # 제품 가격의 통화
    region = models.CharField(max_length=150)  # 라플의 지역
    product = models.ForeignKey('products.kicks', on_delete=models.CASCADE, related_name='release_infos')
    raffle_url = models.CharField(max_length=1000)  # 라플의 도메인
    site_name = models.CharField(max_length=150)  # 라플의 이름
    shipping_method = models.CharField(max_length=150)  # 라플의 배송 방식
