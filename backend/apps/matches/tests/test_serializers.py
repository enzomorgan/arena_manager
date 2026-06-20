from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.championships.models import Championship
from apps.matches.models import Match, MatchEvent
from apps.matches.serializers import MatchSerializer, MatchEventSerializer
from apps.players.models import Player
from apps.teams.models import Team


class MatchSerializerTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="Tester",
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
        
    def test_match_serializer_returns_expected_fields(self):
        match = Match.objects.create(
            championship=self.championship,
            home_team=self.team_a,
            away_team=self.team_b,
            date=timezone.now(),
            round_number=1,
        )
        
        serializer = MatchSerializer(match)
        
        self.assertIn("id", serializer.data)
        self.assertIn("championship", serializer.data)
        self.assertIn("championship_name", serializer.data)
        self.assertIn("home_team", serializer.data)
        self.assertIn("home_team_name", serializer.data)
        self.assertIn("away_team", serializer.data)
        self.assertIn("away_team_name", serializer.data)
        self.assertIn("date", serializer.data)
        self.assertIn("round_number", serializer.data)
        self.assertIn("home_score", serializer.data)
        self.assertIn("away_score", serializer.data)
        self.assertIn("status", serializer.data)
        self.assertIn("created_at", serializer.data)

        self.assertEqual(serializer.data["championship"], self.championship.id)
        self.assertEqual(serializer.data["championship_name"], self.championship.name)
        self.assertEqual(serializer.data["home_team"], self.team_a.id)
        self.assertEqual(serializer.data["home_team_name"], self.team_a.name)
        self.assertEqual(serializer.data["away_team"], self.team_b.id)
        self.assertEqual(serializer.data["away_team_name"], self.team_b.name)
        
    def test_match_serializer_valid_payload(self):
        payload = {
            "championship": self.championship.id,
            "home_team": self.team_a.id, 
            "away_team": self.team_b.id,
            "date": timezone.now().isoformat(),
            "round_number": 1,
            "home_score": 0,
            "away_score": 0,
            "status": Match.Status.SCHEDULED,
        }
        
        serializer = MatchSerializer(data=payload)
        
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        match = serializer.save()
        
        self.assertEqual(match.championship, self.championship)
        self.assertEqual(match.home_team, self.team_a)
        self.assertEqual(match.away_team, self.team_b)
        self.assertEqual(match.round_number, 1)
        
    def test_match_serializer_requires_championship(self):
        payload = {
            "home_team": self.team_a.id,
            "away_team": self.team_b.id,
            "date": timezone.now().isoformat(),
        }

        serializer = MatchSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("championship", serializer.errors)
        
class MatchEventSerializerTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="tester2",
            email="tester2@example.com",
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

        self.match = Match.objects.create(
            championship=self.championship,
            home_team=self.team_a,
            away_team=self.team_b,
            date=timezone.now(),
            round_number=1,
        )

    def test_match_event_serializer_returns_expected_fields(self):
        event = MatchEvent.objects.create(
            match=self.match,
            player=self.player_a,
            team=self.team_a,
            event_type=MatchEvent.EventType.GOAL,
            minute=35,
        )

        serializer = MatchEventSerializer(event)

        self.assertIn("id", serializer.data)
        self.assertIn("match", serializer.data)
        self.assertIn("match_description", serializer.data)
        self.assertIn("player", serializer.data)
        self.assertIn("player_name", serializer.data)
        self.assertIn("team", serializer.data)
        self.assertIn("team_name", serializer.data)
        self.assertIn("event_type", serializer.data)
        self.assertIn("minute", serializer.data)
        self.assertIn("created_at", serializer.data)

        self.assertEqual(serializer.data["match"], self.match.id)
        self.assertEqual(serializer.data["player"], self.player_a.id)
        self.assertEqual(serializer.data["player_name"], self.player_a.name)
        self.assertEqual(serializer.data["team"], self.team_a.id)
        self.assertEqual(serializer.data["team_name"], self.team_a.name)
        self.assertEqual(serializer.data["event_type"], MatchEvent.EventType.GOAL)
        self.assertEqual(serializer.data["minute"], 35)

    def test_match_event_serializer_valid_payload(self):
        payload = {
            "match": self.match.id,
            "player": self.player_a.id,
            "team": self.team_a.id,
            "event_type": MatchEvent.EventType.GOAL,
            "minute": 35,
        }

        serializer = MatchEventSerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        event = serializer.save()

        self.assertEqual(event.match, self.match)
        self.assertEqual(event.player, self.player_a)
        self.assertEqual(event.team, self.team_a)
        self.assertEqual(event.event_type, MatchEvent.EventType.GOAL)

    def test_match_event_serializer_requires_event_type(self):
        payload = {
            "match": self.match.id,
            "player": self.player_a.id,
            "team": self.team_a.id,
            "minute": 35,
        }

        serializer = MatchEventSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("event_type", serializer.errors)