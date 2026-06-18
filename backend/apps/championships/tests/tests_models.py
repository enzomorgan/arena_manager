from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.championships.classification_service import (
    recalculate_standings as recalculate_standings_by_object,
)
from apps.championships.models import Championship, Standing
from apps.championships.services import (
    generate_round_robin,
    recalculate_standings as recalculate_standings_by_id,
)
from apps.matches.models import Match, MatchEvent
from apps.players.models import Player
from apps.teams.models import Team



class ChampionshipBackendFlowTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="testpass123",
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.team_a = Team.objects.create(name="Arena FC", city="Pau dos Ferros", manager=self.user)
        self.team_b = Team.objects.create(name="Bola FC", city="Mossoró", manager=self.user)
        self.team_c = Team.objects.create(name="Craques FC", city="Natal", manager=self.user)
        self.team_d = Team.objects.create(name="Dragoões FC", city="Caicó", manager=self.user)
        
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
        
    def test_recalculate_classification_service_by_object(self):
        Match.objects.create(
            championship=self.championship,
            home_team=self.team_a,
            away_team=self.team_b,
            date=timezone.now(),
            home_score=3,
            away_score=1,
            status=Match.Status.FINISHED,
        )
        
        recalculate_standings_by_object(self.championship)
        
        home = Standing.objects.get(
            championship=self.championship,
            team=self.team_a,
        )
        away = Standing.objects.get(
            championship=self.championship,
            team=self.team_b,
        )
        
        self.assertEqual(home.played, 1)
        self.assertEqual(home.wins, 1)
        self.assertEqual(home.points, 3)
        self.assertEqual(home.goals_for, 3)
        self.assertEqual(home.goals_against, 1)

        self.assertEqual(away.played, 1)
        self.assertEqual(away.losses, 1)
        self.assertEqual(away.points, 0)
        self.assertEqual(away.goals_for, 1)
        self.assertEqual(away.goals_against, 3)
        
    def test_recalculate_services_by_id(self):
        Match.objects.create(
            championship=self.championship,
            home_team=self.team_a,
            away_team=self.team_b,
            date=timezone.now(),
            home_score=2,
            away_score=2,
            status=Match.Status.FINISHED,
        )
        
        standings = recalculate_standings_by_id(self.championship.id)
        
        self.assertEqual(standings.count(), 4)
        
        home = Standing.objects.get(
            championship=self.championship,
            team=self.team_a,
        )
        away = Standing.objects.get(
            championship=self.championship,
            team=self.team_b,
        )
        
        self.assertEqual(home.draws, 1)
        self.assertEqual(away.draws, 1)
        self.assertEqual(home.points, 1)
        self.assertEqual(away.points, 1)
        self.assertEqual(home.goals_for, 2)
        self.assertEqual(away.goals_for, 2)
        
    def test_generate_round_robin_creates_matches(self):
        generate_round_robin(self.championship)
        
        matches = Match.objects.filter(championship=self.championship)
        
        self.assertEqual(matches.count(), 6)
        
        for match in matches:
            self.assertIsNotNone(match.home_team)
            self.assertIsNotNone(match.away_team)
            self.assertNotEqual(match.home_team, match.away_team)
            self.assertIsNotNone(match.date)
            
    def test_dashboard_endpoint_returns_summary(self):
        Match.objects.create(
            championship=self.championship,
            home_team=self.team_a,
            away_team=self.team_b,
            date=timezone.now(),
            home_score=1,
            away_score=0,
            status=Match.Status.FINISHED,
        )
        
        recalculate_standings_by_object(self.championship)

        response = self.client.get(
            f"/api/championships/{self.championship.id}/dashboard/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["championship"], self.championship.name)
        self.assertEqual(response.data["teams"], 4)
        self.assertEqual(response.data["matches_played"], 1)
        
    def test_top_scorers_endpoint_returns_goals(self):
        match = Match.objects.create(
            championship=self.championship,
            home_team=self.team_a,
            away_team=self.team_b,
            date=timezone.now(),
            home_score=1,
            away_score=0,
            status=Match.Status.FINISHED,
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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["player__name"], self.player_a.name)
        self.assertEqual(response.data[0]["goals"], 1)