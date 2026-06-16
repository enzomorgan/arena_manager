from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.matches.models import MatchEvent

class TopScorersView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, championship_id):
        
        scorers = (
            MatchEvent.objects.filter(
                match__championship_id=championship_id,
                event_type=MatchEvent.EventType.GOAL,
            )
            .values(
                "player__id",
                "player__name",
                "team__name",
            )
            .annotate(goals=Count("id"))
            .order_by("-goals")[:20]
        )
        
        return Response(scorers)