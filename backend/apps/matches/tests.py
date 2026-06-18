from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from apps.championships.models import Championship
from apps.matches.models import Match, MatchEvent
from apps.players.models import Player
from apps.teams.models import Team

class MatchFlowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="testpass123",
        )
        
        self.client = APIClient()
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
            name="João Goleador",
            nickname="João",
            position=Player.Position.FORWARD,
            team=self.team_a,
        )
        
        self.player_b = Player.objects.create(
            name="Carlos Zagueiro",
            nickname="Carlos",
            position=Player.Position.DEFENDER,
            team=self.team_b,
        )
        
        self.championship = Championship.objects.create(
            name="Campeonato teste",
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
            status=Match.Status.SCHEDULED,
        )
        
    def test_create_goal_event_updates_home_score(self):
        MatchEvent.objects.create(
            match=self.match,
            player=self.player_b,
            team=self.team_b,
            event_type=MatchEvent.EventType.GOAL,
            minute=20,
        )
        
        self.match.refresh_from_db()
        
        self.assertEqual(self.match.home_score, 1)
        self.assertEqual(self.match.away_score, 0)
        
    def test_create_goal_event_updates_away_score(self):
        MatchEvent.objects.create(
            match=self.match,
            player=self.player_b,
            team=self.team_b,
            event_type=MatchEvent.EventType.GOAL,
            minute=20,
        )
        
        self.match.refresh_from_db()
        
        self.assertEqual(self.match.home_score, 0)
        self.assertEqual(self.match.away_score, 1)
        
    def test_card_event_does_not_update_score(self):
        MatchEvent.objects.create(
            match=self.match,
            player=self.player_b,
            team=self.team_b,
            event_type=MatchEvent.EventType.YELLOW_CARD,
            minute=30,
        )
        
        self.match.refresh_from_db()
        
        self.assertEqual(self.match.home_score, 0)
        self.assertEqual(self.match.away_score, 0)
        
    def test_multiple_goal_events_update_score(self):
        MatchEvent.objects.create(
            match=self.match,
            player=self.player_a,
            team=self.team_a,
            event_type=MatchEvent.EventType.GOAL,
            minute=40,
        )
        MatchEvent.objects.create(
            match=self.match,
            player=self.player_b,
            team=self.team_b,
            event_type=MatchEvent.EventType.GOAL,
            minute=60,
        )
        
        self.match.refresh_from_db()
        
        self.assertEqual(self.match.home_score, 2)
        self.assertEqual(self.match.away_score, 1)