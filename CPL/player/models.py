from django.db import models
from django.conf import settings
from team.models import Team
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
    assigned_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
    registered_at = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=100)
    current_price = models.IntegerField(default=0)
    CATEGORY_CHOICES = [
        ('A', 'Category A'),
        ('B', 'Category B'),
        ('C', 'Category C'),
    ]
    player_class = models.CharField(max_length=1, choices=CATEGORY_CHOICES, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Set initial price based on player_class if price is default or zero
        if not self.price or self.price == 100:
            if self.player_class == 'A':
                self.price = 1000
            elif self.player_class == 'B':
                self.price = 700
            elif self.player_class == 'C':
                self.price = 500
            else:
                self.price = 0
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} ({self.batch})"
