from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Championship, Standing
from .serializers import ChampionshipSerializer, StandingSerializer
from .services import recalculate_standings

class ChampionshipViewSet(viewsets.ModelViewSet):
    queryset = Championship.objects.prefetch_related("teams").all()
    serializer_class = ChampionshipSerializer
    permission_classes = [IsAuthenticated]
    
    filterset_fields = ["city", "modality", "format", "is_active"]
    search_fields = ["name", "season", "city"]
    ordering_fields = ["name", "created_at", "start_date"]
    ordering = ["-created_at"]
    
    @action(detail=True, methods=["get"])
    def standings(self, request, pk=None):
        championship = self.get_object()
        
        standings = Standing.objects.filter(
            championship=championship,
        ).select_related("team").order_by(
            "-points",
            "-wins",
            "-goals_for"
        )
        
        serializer = StandingSerializer(standings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"], url_path="recalcute-standings")
    def recalculate(self, request, pk=None):
        championship = self.get_object()
        standings = recalculate_standings(championship.id)
        
        serializer = StandingSerializer(standings, many=True)
        return Response(serializer.data)
    
class StandingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Standing.objects.select_related("championship", "team").all()
    serializer_class = StandingSerializer
    permission_classes = [IsAuthenticated]
    
    filterset_fields = ["championship", "team"]
    search_fields = ["team__name", "championship__name"]
    ordering_fields = ["points", "wins", "goals_for"]
    ordering = ["-points", "-wins", "-goals_for"]