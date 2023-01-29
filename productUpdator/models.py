from django.db import models
from products.models import kicks as product
from django.conf import settings




# Create your models here.
class ProductUpdator(models.Model):
    """_summary_
        ProductUpdator model 은 유저가 각 제품에 대한 추가 정보를 담고 있습니다.
        일종의 게시판과 같이 작동한다
    Args:
        models (_type_): _description_
    """
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id  = models.ForeignKey(product, on_delete=models.CASCADE, related_name='productUpdator')
    
    
    
class ProductUpdatorItems(models.Model):
    """_summary_
        위 productUpdator 모델당 여러개의 업데이트 정보를 갖는다 . 
        게시글의 댓글과 같은 역할을 한다.
    Args:
        models (_type_): _description_
    """
    product_updator_id = models.ForeignKey(ProductUpdator, on_delete=models.CASCADE, related_name='productUpdatorItems')
    field_name  = models.CharField(max_length=100, null=False, blank=False,)
    field_value = models.CharField(max_length=2500, null=False, blank=False,)
    image       = models.ImageField(upload_to='productUpdator/', null=True, blank=True)
    aproved     = models.BooleanField(default=False) # 제품 정보 업데이트 요청이 승인되었는지 여부
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

