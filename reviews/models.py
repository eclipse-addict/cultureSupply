from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import kicks
from accounts.models import UserInfo


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    product = models.ForeignKey(kicks, related_name='reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True, null=True)  # 별점
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='review_like_users', blank=True)
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='review_dislike_users', blank=True)
