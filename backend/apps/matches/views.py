from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Match, MatchEvent
from .serializers import MatchSerializer, MatchEventSerializer

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.select_related(
        "championship",
        "home_team",
        "away_team",
    ).all()
    
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]
    
    filterset_fields = [
        "championship",
        "home_team",
        "away_team",
        "status",
        "round_number",
    ]
    
    search_fields = [
        "championship__name",
        "home_team__name",
        "away_team__name",
    ]
    
    ordering_fields = [
        "date",
        "round_number",
        "created_at",
    ]
    
class MatchEventViewSet(viewsets.ModelViewSet):
    queryset = MatchEvent.objects.select_related(
        "match",
        "player",
        "team",
    ).all()
    
    serializer_class = MatchEventSerializer
    permission_classes = [IsAuthenticated]
    
    filterset_fields = [
        "match",
        "player",
        "team",
        "event_type",
    ]
    
    search_filds = [
        "player__name",
        "player__nickname",
        "team__name",
    ]
    
    ordering_fields = [
        "minute",
        "created_at",
    ]
    
    ordering = ["match", "minute"]