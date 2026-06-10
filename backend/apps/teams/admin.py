from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "manager", "founded_year")
    search_fields = ("name", "city")
    list_filter = ("city",)