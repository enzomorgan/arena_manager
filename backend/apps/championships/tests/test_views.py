from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.championships.models import Championship
from apps.teams.models import Team


class ChampionshipViewSetTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="123456",
        )
        self.client.force_authenticate(user=self.user)

        self.team_a = Team.objects.create(
            name="Arena FC",
            city="Pau dos Ferros",
            manager=self.user,
        )
        self.team_b = Team.objects.create(
            name="Bola FC",
            city="Mossoró",
            manager=self.user,
        )

    def test_create_championship(self):
        response = self.client.post(
            "/api/championships/",
            {
                "name": "Campeonato Teste",
                "season": "2026",
                "city": "Pau dos Ferros",
                "modality": Championship.Modality.FOOTBALL,
                "format": Championship.Format.LEAGUE,
                "teams": [self.team_a.id, self.team_b.id],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Championship.objects.count(), 1)
        self.assertEqual(Championship.objects.first().teams.count(), 2)

    def test_list_championships(self):
        championship = Championship.objects.create(
            name="Campeonato Teste",
            season="2026",
            city="Pau dos Ferros",
            modality=Championship.Modality.FOOTBALL,
            format=Championship.Format.LEAGUE,
        )
        championship.teams.set([self.team_a, self.team_b])

        response = self.client.get("/api/championships/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_championship(self):
        championship = Championship.objects.create(
            name="Campeonato Teste",
            season="2026",
            city="Pau dos Ferros",
            modality=Championship.Modality.FOOTBALL,
            format=Championship.Format.LEAGUE,
        )

        response = self.client.patch(
            f"/api/championships/{championship.id}/",
            {
                "name": "Campeonato Atualizado",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        championship.refresh_from_db()
        self.assertEqual(championship.name, "Campeonato Atualizado")

    def test_delete_championship(self):
        championship = Championship.objects.create(
            name="Campeonato Teste",
            season="2026",
            city="Pau dos Ferros",
            modality=Championship.Modality.FOOTBALL,
            format=Championship.Format.LEAGUE,
        )

        response = self.client.delete(
            f"/api/championships/{championship.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Championship.objects.count(), 0)

    def test_unauthenticated_user_cannot_list_championships(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/championships/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)