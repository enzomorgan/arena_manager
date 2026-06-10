from django.contrib import admin
from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "nickname", "team", "position", "city", "is_active")
    search_fields = ("name", "nickname", "city", "team__name")
    list_filter = ("position", "city", "is_active")