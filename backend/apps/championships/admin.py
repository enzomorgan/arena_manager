from django.contrib import admin
from .models import Championship, Standing
from .services import recalculate_standings

@admin.register(Championship)
class ChampionshipAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "season",
        "city",
        "modality",
        "format",
        "is_active",
    )
    
    search_fields = (
        "name",
        "season",
        "city",
    )
    
    list_filter = (
        "modality",
        "format",
        "city",
        "is_active",
    )
    
    filter_horizontal = (
        "teams",
    )
    
@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    list_display = (
        "championship",
        "team",
        "points",
        "played",
        "wins",
        "draws",
        "losses",
        "goals_for",
        "goals_against",
        "goal_difference",
    )

    list_filter = ("championship",)
    search_fields = ("team__name", "championship__name")