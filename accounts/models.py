from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    # nessary for registration
    email = models.EmailField(verbose_name='email')
    gender = models.SmallIntegerField(null=True, blank=True)
    phoneNumber = models.CharField(max_length=11)
    
    # Optional fields
    topSize = models.SmallIntegerField(null=True)
    shoeSize = models.SmallIntegerField(null=True)
    bottomSize = models.SmallIntegerField(null=True)
    

    
