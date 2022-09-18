from django import forms
from django.forms import Form, ModelForm, DateField, widgets
from .models import Sneaker

class SneakerForm(forms.ModelForm):
    
    class Meta:
        model = Sneaker
        exclude = ('user', 'like_users',)
        widgets = {
            'release_date' : widgets.DateInput(attrs={'type': 'date'})
        }
