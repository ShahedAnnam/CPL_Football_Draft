from django import forms
from django.contrib.auth import get_user_model
from .models import Player

User = get_user_model()  # Use your custom user model

class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'age', 'playing_position', 'batch', 'contact_number', 'profile_picture']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your age'}),
            'playing_position': forms.Select(attrs={'class': 'form-control'}),
            'batch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 48th'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your contact number'}),
        }
