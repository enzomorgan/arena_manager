from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.players.models import Player
from apps.teams.models import Team


class PlayerViewSetTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="123456",
        )
        self.client.force_authenticate(user=self.user)

        self.team = Team.objects.create(
            name="Arena FC",
            city="Pau dos Ferros",
            manager=self.user,
        )

    def test_create_player(self):
        response = self.client.post(
            "/api/players/",
            {
                "name": "João",
                "nickname": "J",
                "position": Player.Position.FORWARD,
                "team": self.team.id,
                "city": "Pau dos Ferros",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(Player.objects.first().name, "João")

    def test_list_players(self):
        Player.objects.create(
            name="João",
            nickname="J",
            position=Player.Position.FORWARD,
            team=self.team,
        )

        response = self.client.get("/api/players/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_player(self):
        player = Player.objects.create(
            name="João",
            nickname="J",
            position=Player.Position.FORWARD,
            team=self.team,
        )

        response = self.client.patch(
            f"/api/players/{player.id}/",
            {
                "nickname": "Joãozinho",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        player.refresh_from_db()
        self.assertEqual(player.nickname, "Joãozinho")

    def test_delete_player(self):
        player = Player.objects.create(
            name="João",
            nickname="J",
            position=Player.Position.FORWARD,
            team=self.team,
        )

        response = self.client.delete(f"/api/players/{player.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Player.objects.count(), 0)

    def test_unauthenticated_user_cannot_list_players(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/players/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)