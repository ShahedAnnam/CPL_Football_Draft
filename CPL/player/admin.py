from django.contrib import admin
from .models import Player

# Register Player without custom admin class
admin.site.register(Player)
