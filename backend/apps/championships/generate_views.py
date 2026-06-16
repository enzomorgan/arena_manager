from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.championships.models import Championship
from apps.championships.services import generate_round_robin


class GenerateMatchesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, championship_id):

        championship = Championship.objects.get(
            pk=championship_id
        )

        generate_round_robin(championship)

        return Response(
            {
                "message": "Tabela gerada com sucesso."
            }
        )