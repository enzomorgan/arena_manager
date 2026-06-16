from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.championships.models import Championship, Standing
from apps.matches.models import Match, MatchEvent

class ChampionshipDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, championship_id):
        
        championship = Championship.objects.get(
            pk=championship_id
        )
        
        standings = Standing.objects.filter(
            championship=championship
        ).order_by(
            "-points",
            "-goal_difference",
        )
        
        leader = standings.first()
        
        matches_played = Match.objects.filter(
            championship=championship,
            status="FINISHED",
        ).count()
        
        matches_remaining = Match.objects.filter(
            championship=championship,
        ).exclude(
            status="FINISHED"
        ).count()
        
        top_score = (
            MatchEvent.objects.filter(
                match__championship=championship,
                event_type=MatchEvent.EventType.GOAL,
            )
            .values(
                "player__name",
                "team__name",
            )
            .annotate(goals=Count("id"))
            .order_by("-goals")
            .first()
        )
        
        next_matches = Match.objects.filter(
            championship=championship
        ).exclude(
            status="FINISHED"
        )[:5]
        
        return Response(
            {
                "championship": championship.name,
                "teams": championship.teams.count(),
                "matches_played": matches_played,
                "matches_remaining": matches_remaining,
                
                "leader": (
                    {
                        "team": leader.team.name,
                        "point": leader.points,
                    }
                    if leader
                    else None
                ),
                
                "top_scorer": top_score,
                
                "next_matches": [
                    {
                        "id": match.id,
                        "home_team": match.home_team.name,
                        "away_team": match.away_team.name,
                        "date": match.date,
                    }
                    for match in next_matches
                ],
            }
        )