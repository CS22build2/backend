from django.contrib import admin

# Register your models here.
from .models import Player, Room


admin.site.register(Player)
admin.site.register(Room)
