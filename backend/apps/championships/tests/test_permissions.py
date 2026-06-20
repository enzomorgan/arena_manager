from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.championships.models import Championship
from apps.matches.models import Match, MatchEvent
from apps.players.models import Player
from apps.teams.models import Team


class ChampionshipPermissionTests(APITestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="123456",
        )

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

        self.player = Player.objects.create(
            name="João",
            nickname="J",
            position=Player.Position.FORWARD,
            team=self.team_a,
        )

        self.championship = Championship.objects.create(
            name="Campeonato Teste",
            season="2026",
            city="Pau dos Ferros",
            modality=Championship.Modality.FOOTBALL,
            format=Championship.Format.LEAGUE,
        )
        self.championship.teams.set([self.team_a, self.team_b])

        self.match = Match.objects.create(
            championship=self.championship,
            home_team=self.team_a,
            away_team=self.team_b,
            date=timezone.now(),
            round_number=1,
        )

    def test_unauthenticated_user_cannot_list_championships(self):
        response = self.client.get("/api/championships/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_create_championship(self):
        response = self.client.post(
            "/api/championships/",
            {
                "name": "Copa Arena",
                "season": "2026",
                "city": "Mossoró",
                "modality": Championship.Modality.FOOTBALL,
                "format": Championship.Format.LEAGUE,
                "teams": [self.team_a.id, self.team_b.id],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Championship.objects.count(), 1)

    def test_unauthenticated_user_cannot_update_championship(self):
        response = self.client.patch(
            f"/api/championships/{self.championship.id}/",
            {
                "name": "Nome Alterado",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.championship.refresh_from_db()
        self.assertEqual(self.championship.name, "Campeonato Teste")

    def test_unauthenticated_user_cannot_delete_championship(self):
        response = self.client.delete(
            f"/api/championships/{self.championship.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Championship.objects.count(), 1)

    def test_unauthenticated_user_cannot_generate_matches(self):
        response = self.client.post(
            f"/api/championships/{self.championship.id}/generate-matches/"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_recalculate_standings(self):
        response = self.client.post(
            f"/api/championships/{self.championship.id}/recalculate/"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_access_dashboard(self):
        response = self.client.get(
            f"/api/championships/{self.championship.id}/dashboard/"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_access_top_scorers(self):
        MatchEvent.objects.create(
            match=self.match,
            player=self.player,
            team=self.team_a,
            event_type=MatchEvent.EventType.GOAL,
            minute=35,
        )

        response = self.client.get(
            f"/api/championships/{self.championship.id}/top-scorers/"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)