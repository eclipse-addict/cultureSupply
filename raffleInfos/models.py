from django.db import models
from products.models import kicks
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Raffle(models.Model):
    title         = models.CharField(max_length=500, null=False, blank=True) 
    product       = models.ForeignKey(kicks, related_name='raffles', on_delete=models.CASCADE)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    due_date      = models.DateTimeField()
    point_cost    = models.PositiveIntegerField(default=0, blank=False, null=False)   
    rating        = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True, null=True)  # 별점
    like_users    = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='raffle_like_users', blank=True)
    


class RaffleEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    created_at    = models.DateTimeField(auto_now_add=True)
