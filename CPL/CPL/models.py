from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('player', 'Player'),
        ('team_owner', 'Team Owner'),
        ('authority', 'Authority'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
