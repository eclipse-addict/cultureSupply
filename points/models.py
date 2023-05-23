from django.db import models
from django.conf import settings


# Create your models here.
class Point(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_points = models.IntegerField(default=0)
    used_points = models.IntegerField(default=0)


class PointHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    point_type = models.CharField(max_length=500, blank=False, null=False)  # charge, use
    point_amount = models.IntegerField(default=0, blank=False, null=False)
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
