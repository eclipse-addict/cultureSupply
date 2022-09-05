from django import forms
from .models import Sneaker

class SneakerForm(forms.ModelForm):
    
    class Meta:
        model = Sneaker
        exclude = ('user',)
