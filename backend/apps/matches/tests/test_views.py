from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.championships.models import Championship
from apps.matches.models import Match, MatchEvent
from apps.players.models import Player
from apps.teams.models import Team


class MatchViewSetTests(APITestCase):
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

        self.player_a = Player.objects.create(
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

    def test_create_match(self):
        response = self.client.post(
            "/api/matches/",
            {
                "championship": self.championship.id,
                "home_team": self.team_a.id,
                "away_team": self.team_b.id,
                "date": timezone.now().isoformat(),
                "round_number": 1,
                "status": Match.Status.SCHEDULED,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), 1)

    def test_list_matches(self):
        Match.objects.create(
            championship=self.championship,
            home_team=self.team_a,
            away_team=self.team_b,
            date=timezone.now(),
            round_number=1,
        )

        response = self.client.get("/api/matches/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_match_score_and_status(self):
        match = Match.objects.create(
            championship=self.championship,
            home_team=self.team_a,
            away_team=self.team_b,
            date=timezone.now(),
            round_number=1,
        )

        response = self.client.patch(
            f"/api/matches/{match.id}/",
            {
                "home_score": 2,
                "away_score": 1,
                "status": Match.Status.FINISHED,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        match.refresh_from_db()
        self.assertEqual(match.home_score, 2)
        self.assertEqual(match.away_score, 1)
        self.assertEqual(match.status, Match.Status.FINISHED)

    def test_create_match_event_goal_updates_score(self):
        match = Match.objects.create(
            championship=self.championship,
            home_team=self.team_a,
            away_team=self.team_b,
            date=timezone.now(),
            round_number=1,
        )

        response = self.client.post(
            "/api/match-events/",
            {
                "match": match.id,
                "player": self.player_a.id,
                "team": self.team_a.id,
                "event_type": MatchEvent.EventType.GOAL,
                "minute": 35,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        match.refresh_from_db()
        self.assertEqual(match.home_score, 1)
        self.assertEqual(match.away_score, 0)

    def test_unauthenticated_user_cannot_list_matches(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/matches/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)