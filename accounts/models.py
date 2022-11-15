from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)

class UserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        print('create_user')
        if not email:
            raise ValueError('The Email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=300, null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=100, null=False, blank=False,)
    last_name = models.CharField(max_length=100, null=False, blank=False,)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
class UserExtraInfo(models.Model):
    pass