from django.db import models

# Create your models here. 

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
    
    
