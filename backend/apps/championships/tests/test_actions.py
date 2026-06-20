from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.championships.models import Championship, Standing
from apps.matches.models import Match, MatchEvent
from apps.players.models import Player
from apps.teams.models import Team



class ChampionshipActionTests(APITestCase):
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
        self.team_c = Team.objects.create(
            name="Craques FC",
            city="Natal",
            manager=self.user,
        )
        self.team_d = Team.objects.create(
            name="Dragões FC",
            city="Caicó",
            manager=self.user,
        )

        self.player_a = Player.objects.create(
            name="João Goleador",
            nickname="João",
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
        self.championship.teams.set([
            self.team_a,
            self.team_b,
            self.team_c,
            self.team_d,
        ])
        
    def test_generate_matches_endpoint(self):
        response = self.client.post(
            f"/api/championships/{self.championship.id}/generate-matches/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Match.objects.filter(championship=self.championship).count(),
            6,
        )

    def test_recalculate_standings_endpoint(self):
        Match.objects.create(
            championship=self.championship,
            home_team=self.team_a,
            away_team=self.team_b,
            date=timezone.now(),
            home_score=2,
            away_score=1,
            status=Match.Status.FINISHED,
        )

        response = self.client.post(
            f"/api/championships/{self.championship.id}/recalculate/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        standing = Standing.objects.get(
            championship=self.championship,
            team=self.team_a,
        )

        self.assertEqual(standing.points, 3)
        self.assertEqual(standing.goals_for, 2)
        self.assertEqual(standing.goals_against, 1)

    def test_dashboard_endpoint(self):
        Match.objects.create(
            championship=self.championship,
            home_team=self.team_a,
            away_team=self.team_b,
            date=timezone.now(),
            home_score=1,
            away_score=0,
            status=Match.Status.FINISHED,
        )

        response = self.client.get(
            f"/api/championships/{self.championship.id}/dashboard/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["championship"], self.championship.name)
        self.assertEqual(response.data["teams"], 4)
        self.assertEqual(response.data["matches_played"], 1)

    def test_top_scorers_endpoint(self):
        match = Match.objects.create(
            championship=self.championship,
            home_team=self.team_a,
            away_team=self.team_b,
            date=timezone.now(),
            status=Match.Status.SCHEDULED,
        )

        MatchEvent.objects.create(
            match=match,
            player=self.player_a,
            team=self.team_a,
            event_type=MatchEvent.EventType.GOAL,
            minute=35,
        )

        response = self.client.get(
            f"/api/championships/{self.championship.id}/top-scorers/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["player__name"], self.player_a.name)
        self.assertEqual(response.data[0]["goals"], 1)

    def test_unauthenticated_user_cannot_generate_matches(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(
            f"/api/championships/{self.championship.id}/generate-matches/"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)