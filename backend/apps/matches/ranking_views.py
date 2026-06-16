from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.matches.views import MatchEvent

class BaseEventRankingView(APIView):
    permission_classes = [IsAuthenticated]
    event_type = None
    result_field = "total"
    
    def get(self, request):
        championship_id = request.query_params.get("championship")
        
        events = MatchEvent.objects.filter(
            event_type=self.event_type,
        )
        
        if championship_id:
            events = events.filter(
                match__championship_id=championship_id
            )
            
        ranking = (
            events.values(
                "player_id",
                "player__name",
                "player__nickname",
                "team_id",
                "team__name",
            )
            .annotate(**{self.result_field: Count("id")})
            .order_by(f"-{self.result_field}", "player__name")
        )
        
        return Response(ranking)
    
class TopScorersView(BaseEventRankingView):
    event_type = MatchEvent.EventType.GOAL
    result_field = "goals"
    
class TopAssistsView(BaseEventRankingView):
    event_type = MatchEvent.EventType.ASSIST
    result_field = "assists"
    
class YellowCardsRankingView(BaseEventRankingView):
    event_type = MatchEvent.EventType.YELLOW_CARD
    result_field = "yellow_cards"
    
class RedCardsRankingView(BaseEventRankingView):
    event_type = MatchEvent.EventType.RED_CARD
    result_field = "red_cards"