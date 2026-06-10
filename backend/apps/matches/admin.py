from django.contrib import admin
from .models import Match

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "championship",
        "home_team",
        "away_team",
        "date",
        "round_number",
        "home_score",
        "away_score",
        "status",
    )
    
    search_fields = (
        "championship__name",
        "home_team__name",
        "away_team__name",
    )
    
    list_filter = (
        "status",
        "championship",
        "round_number",
    )