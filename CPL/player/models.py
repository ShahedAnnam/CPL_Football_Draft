from django.db import models
from django.conf import settings
import team
class Player(models.Model):
    
    POSITION_CHOICES = [
        ('Midfielder', 'Midfielder'),
        ('Goalkeeper', 'Goalkeeper'),
        ('Forward', 'Forward'),
        ('Defender', 'Defender'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    playing_position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    batch = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    assigned_team = models.CharField(max_length=100, default="Not bought yet")
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.batch})"
