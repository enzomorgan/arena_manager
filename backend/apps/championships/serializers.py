from rest_framework import serializers
from .models import Championship, Standing

class ChampionshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Championship
        fields = [
            "id",
            "name",
            "season",
            "city",
            "modality",
            "format",
            "teams",
            "start_date",
            "end_date",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
        
class StandingSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source="team.name", read_only=True)
    goal_difference = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Standing
        fields = [
            "id",
            "championship",
            "team",
            "team_name",
            "played",
            "wins",
            "draws",
            "losses",
            "goals_for",
            "goals_against",
            "goal_difference",
            "points",
        ]
        read_only_fields = [
            "id",
            "team_name",
            "goal_difference",
        ]