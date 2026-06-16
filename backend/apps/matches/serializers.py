from rest_framework import serializers
from .models import Match, MatchEvent

class MatchSerializer(serializers.ModelSerializer):
    home_team_name = serializers.CharField(source="home_team.name", read_only=True)
    away_team_name = serializers.CharField(source="away_team.name", read_only=True)
    championship_name = serializers.CharField(source="championship.name", read_only=True)
    
    class Meta:
        model = Match
        fields = [
            "id", 
            "championship",
            "championship_name",
            "home_team",
            "home_team_name",
            "away_team",
            "away_team_name",
            "date",
            "round_number",
            "home_score",
            "away_score",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "home_team_name",
            "away_team_name",
            "championship_name",
        ]
        
class MatchEventSerializer(serializers.ModelSerializer):
    match_description = serializers.CharField(source="match.__str__", read_only=True)
    player_name = serializers.CharField(source="player.name", read_only=True)
    team_name = serializers.CharField(source="team.name", read_only=True)
    
    class Meta:
        model = MatchEvent
        fields = [
            "id",
            "match",
            "match_description",
            "player",
            "player_name",
            "team",
            "team_name",
            "event_type",
            "minute",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "match_description",
            "player_name",
            "team_name",
            "created_at",
        ]