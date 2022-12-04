from django.db import models
from django.conf import settings


class kicks(models.Model):
    # uuid that stock asigned for this product 
    # it's used to determine whether it's already in stock on the database
    uuid                 = models.CharField(max_length=100, )
    brand                = models.CharField(max_length=100, )
    colorway             = models.CharField(max_length=150, )
    countryOfManufacture = models.CharField(max_length=100, )
    dataType             = models.CharField(max_length=100, )
    description          = models.TextField()
    gender               = models.CharField(max_length=10, )
    name                 = models.CharField(max_length=500, )
    productCategory      = models.CharField(max_length=100, )
    releaseDate          = models.CharField(max_length=100)
    retailPrice          = models.PositiveBigIntegerField()
    estimatedMarketValue = models.PositiveBigIntegerField(default=0)
    title                = models.CharField(max_length=300, )
    sku                  = models.CharField(max_length=200, default=' ') # ex) 555088-101
    
    imageUrl             = models.CharField(max_length=500, )
    smallImageUrl        = models.CharField(max_length=500, )
    thumbUrl             = models.CharField(max_length=500, )
    
    local_imageUrl             = models.CharField(max_length=500, default='http://localhost:8000/media/images/defaultImg.png')
    local_smallImageUrl        = models.CharField(max_length=500, default=' ')
    local_thumbUrl             = models.CharField(max_length=500, default=' ')
    
    like_users   = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_users', blank=True)

    
