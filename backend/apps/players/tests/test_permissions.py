from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.players.models import Player
from apps.teams.models import Team


class PlayerPermissionTests(APITestCase):
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

        self.player = Player.objects.create(
            name="João",
            nickname="J",
            position=Player.Position.FORWARD,
            team=self.team,
        )

    def test_unauthenticated_user_cannot_list_players(self):
        response = self.client.get("/api/players/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_create_player(self):
        response = self.client.post(
            "/api/players/",
            {
                "name": "Carlos",
                "nickname": "C",
                "position": Player.Position.DEFENDER,
                "team": self.team.id,
                "city": "Mossoró",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Player.objects.count(), 1)

    def test_unauthenticated_user_cannot_update_player(self):
        response = self.client.patch(
            f"/api/players/{self.player.id}/",
            {
                "nickname": "Joãozinho",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.player.refresh_from_db()
        self.assertEqual(self.player.nickname, "J")

    def test_unauthenticated_user_cannot_delete_player(self):
        response = self.client.delete(f"/api/players/{self.player.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Player.objects.count(), 1)