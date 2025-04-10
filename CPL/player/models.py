from django.db import models
from django.contrib.auth.models import User  # For authentication

class Player(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    POSITION_CHOICES = [
        ('Midfielder', 'Midfielder'),
        ('Striker', 'Striker'),
        ('Goalkeeper', 'Goalkeeper'),
        ('Forward', 'Forward'),
        ('Defender', 'Defender'),
        ('Winger', 'Winger'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link with Django Auth
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField()
    playing_position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    batch = models.CharField(max_length=10)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.batch})"
