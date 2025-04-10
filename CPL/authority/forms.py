from django import forms
from .models import PlayerCategory
from player.models import Player

class PlayerCategoryForm(forms.ModelForm):
    player = forms.ModelChoiceField(
        queryset=Player.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PlayerCategory
        fields = ['player', 'category', 'base_price']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
