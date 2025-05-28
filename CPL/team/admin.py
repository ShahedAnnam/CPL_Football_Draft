from django.contrib import admin
from .models import Team

# Register Player without custom admin class
admin.site.register(Team)
