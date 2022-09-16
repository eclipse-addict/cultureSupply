from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
# Create your models here.

class User(AbstractUser):
    # nessary for registration
    GENDER_CHOICES = ('M', 'Male'), ('F', 'Female')
    CLOTHES_SIZE = ('xs', 'XS'), ('sm','S'), ('md', 'M'), ('lg', 'L'), ('xlg', 'XL'),('xxlg', 'XXL'),('xxxlg', 'XXXL'),
    SHOE_SIZE = ('200', 200), ('205',205), ('210', 210), ('220', 220), ('230', 230), ('240', 240), ('250', 250), ('260', 260), ('270', 270), ('280', 280), ('290', 280), ('300', 300), ('300', 300), ('310', 310),
    
    email = models.EmailField(verbose_name='email')
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES, null=True,)
    phoneNumber = models.CharField(max_length=15)
    profile_img = models.ImageField(upload_to='images/user/', null=True, blank=True)

    
    # Optional fields
    
    shoeSize = models.CharField(max_length=10, choices=SHOE_SIZE)
    topSize = models.CharField(max_length=10, choices=CLOTHES_SIZE)
    bottomSize = models.CharField(max_length=10, choices=CLOTHES_SIZE)
    

    
