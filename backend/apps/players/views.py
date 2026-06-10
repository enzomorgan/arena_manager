from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Player
from .serializers import PlayerSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]
    
    filterset_fields = [
        "team",
        "position",
        "city",
        "is_active",
    ]
    
    search_fields = [
        "name",
        "nickname",
        "city",
        "team__name",
    ]
    
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]