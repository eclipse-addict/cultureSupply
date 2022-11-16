from django.db import models
from django.conf import settings

# Create your models here.
# main model of the project
class Sneaker(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # regist user
    model_name   = models.CharField(max_length=255)
    release_date = models.DateField()
    describtion  = models.TextField()
    retail_price = models.CharField( max_length=100)
    like_users   = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_users', blank=True)

class Image(models.Model):
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)
    image   = models.ImageField(upload_to='images/sneakers/%Y/%m/%d/', blank=True, null=True)    
    # main_img = models.BooleanField()
    
