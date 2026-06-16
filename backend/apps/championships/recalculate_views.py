from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.championships.models import Championship
from apps.championships.classification_service import (recalculate_standings)

class RecalculateStandingsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, championship_id):
        championship = Championship.objects.get(
            pk=championship_id
        )
        
        recalculate_standings(championship)
        
        return Response(
            {
                "message": "Classificação atualizada."
            }
        )