from django.db import models
from player.models import Player

class PlayerCategory(models.Model):
    CATEGORY_CHOICES = [
        ('A', 'Category A'),
        ('B', 'Category B'),
        ('C', 'Category C'),
    ]
    
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    assigned_at = models.DateTimeField(auto_now=True)
    
    budget_of_teams = models.IntegerField(default=10000);

    def __str__(self):
        return f"{self.player.name} - {self.get_category_display()} (${self.base_price})"
