from rest_framework import serializers
from .models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "city",
            "founded_year",
            "shield",
            "manager",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]