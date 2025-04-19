# cpl/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[('', 'Select your role')] + list(CustomUser.ROLE_CHOICES),
        required=True
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'role', 'password1', 'password2')
