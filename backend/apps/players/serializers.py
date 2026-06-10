from rest_framework import serializers
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            "id",
            "name",
            "nickname",
            "birth_date",
            "position",
            "team",
            "photo",
            "city",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]