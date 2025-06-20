from django.db import models
from django.contrib.auth import get_user_model
import player

User = get_user_model()

class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slogan = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='team_logos/')
    profile_pic = models.ImageField(upload_to='team_profiles/')
    def __str__(self):
        return self.user.username
