from django import forms
from django.contrib.auth.models import User
from .models import Player

class PlayerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Player
        fields = ['name', 'gender', 'age', 'playing_position', 'batch']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'playing_position': forms.Select(attrs={'class': 'form-control'}),
            'batch': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        player = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['name'].lower().replace(" ", "_"),  # Auto-generate username
            password=self.cleaned_data['password']
        )
        player.user = user
        if commit:
            player.save()
        return player
