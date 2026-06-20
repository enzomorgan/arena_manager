from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.players.models import Player
from apps.players.serializers import PlayerSerializer
from apps.teams.models import Team


class PlayerSerializerTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="123456",
        )

        self.team = Team.objects.create(
            name="Arena FC",
            city="Pau dos Ferros",
            manager=self.user,
        )

    def test_player_serializer_returns_expected_fields(self):
        player = Player.objects.create(
            name="João",
            nickname="J",
            position=Player.Position.FORWARD,
            team=self.team,
            city="Pau dos Ferros",
        )

        serializer = PlayerSerializer(player)

        self.assertIn("id", serializer.data)
        self.assertIn("name", serializer.data)
        self.assertIn("nickname", serializer.data)
        self.assertIn("position", serializer.data)
        self.assertIn("team", serializer.data)
        self.assertIn("city", serializer.data)
        self.assertIn("is_active", serializer.data)
        self.assertIn("created_at", serializer.data)

        self.assertEqual(serializer.data["name"], "João")
        self.assertEqual(serializer.data["nickname"], "J")
        self.assertEqual(serializer.data["team"], self.team.id)
        self.assertEqual(serializer.data["is_active"], True)

    def test_player_serializer_valid_payload(self):
        payload = {
            "name": "Carlos",
            "nickname": "C",
            "position": Player.Position.DEFENDER,
            "team": self.team.id,
            "city": "Mossoró",
        }

        serializer = PlayerSerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        player = serializer.save()

        self.assertEqual(player.name, "Carlos")
        self.assertEqual(player.team, self.team)

    def test_player_serializer_requires_name(self):
        payload = {
            "nickname": "Sem Nome",
            "position": Player.Position.FORWARD,
            "team": self.team.id,
        }

        serializer = PlayerSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)