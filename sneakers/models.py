from platform import release
from pydoc import describe
from django.db import models
from django.conf import settings

# Create your models here.
# main model of the project
class Sneaker():
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    release_date = models.DateTimeField()
    describtion = models.TextField()
