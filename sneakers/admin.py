from django.contrib import admin
from .models import Sneaker, Images
# Register your models here.

class imageInline(admin.TabularInline):
    model = Images
    
class SneakerAdmin(admin.ModelAdmin):
    inlines = [imageInline, ]
    
admin.site.register(Sneaker, SneakerAdmin)