from django.db import models

# Create your models here. 

class kicks(models.Model):
    uuid = models.CharField(max_length=100, blank=False, null=False) # uuid that stock asigned for this product 
    brand = models.CharField(max_length=100, blank=False, null=False)
    category = models.CharField(max_length=300, blank=False, null=False)
    colorway = models.CharField(max_length=150, blank=False, null=False)
    countryOfManufacture = models.CharField(max_length=100, blank=False, null=False)
    dataType = models.CharField(max_length=100, default='product', blank=False, null=False)
    describtion = models.TextField()
    gender = models.CharField(max_length=10, blank=False, null=False)
    name = models.CharField(max_length=500, blank=False, null=False)
    productCategory = models.CharField(max_length=100, blank=False, null=False)
    releaseDate = models.DateField()
    retailPrice = models.PositiveBigIntegerField()
    shoe = models.CharField(max_length=100, blank=False, null=False)
    title = models.CharField(max_length=300, blank=False, null=False)
    styleId = models.CharField(max_length=100, blank=False, null=False) # ex) 555088-101
    
    imageUrl = models.CharField(max_length=500, blank=False, null=False)
    smallImageUrl = models.CharField(max_length=500, blank=False, null=False)
    thumbUrl = models.CharField(max_length=500, blank=False, null=False)
    
    
