from django.db import models
from django.conf import settings

# Create your models here.
# main model of the project
class Sneaker(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=255)
    release_date = models.DateField()
    describtion  = models.TextField()
    retail_price = models.CharField( max_length=100)
    img          = models.ImageField(upload_to='images/sneakers/')

    
    
