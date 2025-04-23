from django import forms
from django.contrib.auth import get_user_model
from .models import Player

User = get_user_model()  # ✅ Use your custom user model

class PlayerRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False  # Optional during update
    )

    class Meta:
        model = Player
        fields = ['name', 'age', 'playing_position', 'batch']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'playing_position': forms.Select(attrs={'class': 'form-control'}),
            'batch': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        player = super().save(commit=False)

        # Only create a new user if this is a new player
        if self.instance.pk is None:
            user = User.objects.create_user(
                username=self.cleaned_data['name'].lower().replace(" ", "_"),
                password=self.cleaned_data['password'] or "default123"
            )
            player.user = user

        if commit:
            player.save()
        return player
