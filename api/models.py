import uuid
from django.db import models
from django.conf import settings


class ApiType(models.Model):
    api_type = models.IntegerField(max_length=10, default=1)
    api_call_limit = models.BigIntegerField(default=1000)


# Create your models here.
class ApiInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    api_key = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    call_count = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    api_type = models.ForeignKey(ApiType, on_delete=models.CASCADE)
