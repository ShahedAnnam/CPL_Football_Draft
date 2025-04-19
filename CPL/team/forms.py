from django import forms
from .models import TeamProfile

class TeamProfileForm(forms.ModelForm):
    class Meta:
        model = TeamProfile
        fields = ['slogan', 'logo', 'profile_pic']
