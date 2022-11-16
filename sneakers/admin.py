from django.contrib import admin
from .models import Sneaker, Image
# Register your models here.

class imageInline(admin.TabularInline):
    model = Image
    
class SneakerAdmin(admin.ModelAdmin):
    inlines = [imageInline, ]
    
admin.site.register(Sneaker, SneakerAdmin)