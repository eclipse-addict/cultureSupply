from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):

        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):

        superuser = self.create_user(
            email=email,
            password=password,
        )
        
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        
        superuser.save(using=self._db)
        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

	# 헬퍼 클래스 사용
    objects = UserManager()

	# 사용자의 username field는 email으로 설정 (이메일로 로그인)
    USERNAME_FIELD = 'email'
    
    
class UserInfo(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_CHOICES = ('M', 'Male'), ('F', 'Female')
    CLOTHES_SIZE = ('xs', 'XS'), ('sm','S'), ('md', 'M'), ('lg', 'L'), ('xlg', 'XL'),('xxlg', 'XXL'),('xxxlg', 'XXXL'),
    SHOE_SIZE = ('200', 200), ('205',205), ('210', 210), ('220', 220),
    ('230', 230), ('240', 240), ('250', 250), ('260', 260), ('270', 270), ('280', 280),
    ('290', 280), ('300', 300), ('300', 300), ('310', 310),
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default= '', null=True, blank=True)
    shoeSize = models.CharField(max_length=10, choices=SHOE_SIZE, default= '', null=True, blank=True)
    topSize = models.CharField(max_length=10, choices=CLOTHES_SIZE, default= '', null=True, blank=True)
    bottomSize = models.CharField(max_length=10, choices=CLOTHES_SIZE, default= '', null=True, blank=True)