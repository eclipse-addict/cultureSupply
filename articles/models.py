from django.db import models
from django.conf import settings
from django import forms

# Create your models here.
class article(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title      = models.CharField(max_length=50, blank=False)
    content    = models.TextField()
    category   = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    img        = models.ImageField(upload_to='images/',blank=True, null=True)
    
class image(models.Model):
    article = models.ForeignKey(article, on_delete=models.CASCADE)
    # 이미지를 총 5개까지 등록 할 수 있도록 구현 
    url_1 = models.ImageField(upload_to='images/',blank=True, null=True)
    url_2 = models.ImageField(upload_to='images/',blank=True, null=True)
    url_3 = models.ImageField(upload_to='images/',blank=True, null=True)
    url_4 = models.ImageField(upload_to='images/',blank=True, null=True)
    url_5 = models.ImageField(upload_to='images/',blank=True, null=True)
    
    
# class comments 