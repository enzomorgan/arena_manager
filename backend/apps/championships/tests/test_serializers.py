from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.championships.models import Championship, Standing
from apps.championships.serializers import ChampionshipSerializer, StandingSerializer
from apps.teams.models import Team


class ChampionshipSerializerTests(TestCase):
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

    def test_championship_serializer_returns_expected_fields(self):
        championship = Championship.objects.create(
            name="Campeonato Teste",
            season="2026",
            city="Pau dos Ferros",
            modality=Championship.Modality.FOOTBALL,
            format=Championship.Format.LEAGUE,
        )
        championship.teams.set([self.team_a, self.team_b])

        serializer = ChampionshipSerializer(championship)

        self.assertIn("id", serializer.data)
        self.assertIn("name", serializer.data)
        self.assertIn("season", serializer.data)
        self.assertIn("city", serializer.data)
        self.assertIn("modality", serializer.data)
        self.assertIn("format", serializer.data)
        self.assertIn("teams", serializer.data)
        self.assertIn("start_date", serializer.data)
        self.assertIn("end_date", serializer.data)
        self.assertIn("is_active", serializer.data)
        self.assertIn("created_at", serializer.data)

        self.assertEqual(serializer.data["name"], "Campeonato Teste")
        self.assertEqual(serializer.data["season"], "2026")
        self.assertEqual(serializer.data["city"], "Pau dos Ferros")
        self.assertEqual(serializer.data["modality"], Championship.Modality.FOOTBALL)
        self.assertEqual(serializer.data["format"], Championship.Format.LEAGUE)
        self.assertEqual(len(serializer.data["teams"]), 2)

    def test_championship_serializer_valid_payload(self):
        payload = {
            "name": "Copa Arena",
            "season": "2026",
            "city": "Mossoró",
            "modality": Championship.Modality.FOOTBALL,
            "format": Championship.Format.LEAGUE,
            "teams": [self.team_a.id, self.team_b.id],
        }

        serializer = ChampionshipSerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        championship = serializer.save()

        self.assertEqual(championship.name, "Copa Arena")
        self.assertEqual(championship.teams.count(), 2)

    def test_championship_serializer_requires_name(self):
        payload = {
            "season": "2026",
            "city": "Mossoró",
            "modality": Championship.Modality.FOOTBALL,
            "format": Championship.Format.LEAGUE,
            "teams": [self.team_a.id],
        }

        serializer = ChampionshipSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_championship_serializer_requires_modality(self):
        payload = {
            "name": "Copa Arena",
            "season": "2026",
            "city": "Mossoró",
            "format": Championship.Format.LEAGUE,
            "teams": [self.team_a.id],
        }

        serializer = ChampionshipSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("modality", serializer.errors)


class StandingSerializerTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="tester2",
            email="tester2@example.com",
            password="123456",
        )

        self.team = Team.objects.create(
            name="Arena FC",
            city="Pau dos Ferros",
            manager=self.user,
        )

        self.championship = Championship.objects.create(
            name="Campeonato Teste",
            season="2026",
            city="Pau dos Ferros",
            modality=Championship.Modality.FOOTBALL,
            format=Championship.Format.LEAGUE,
        )

    def test_standing_serializer_returns_expected_fields(self):
        standing = Standing.objects.create(
            championship=self.championship,
            team=self.team,
            played=3,
            wins=2,
            draws=1,
            losses=0,
            goals_for=7,
            goals_against=3,
            points=7,
        )

        serializer = StandingSerializer(standing)

        self.assertIn("id", serializer.data)
        self.assertIn("championship", serializer.data)
        self.assertIn("team", serializer.data)
        self.assertIn("team_name", serializer.data)
        self.assertIn("played", serializer.data)
        self.assertIn("wins", serializer.data)
        self.assertIn("draws", serializer.data)
        self.assertIn("losses", serializer.data)
        self.assertIn("goals_for", serializer.data)
        self.assertIn("goals_against", serializer.data)
        self.assertIn("goal_difference", serializer.data)
        self.assertIn("points", serializer.data)

        self.assertEqual(serializer.data["team_name"], self.team.name)
        self.assertEqual(serializer.data["goal_difference"], 4)
        self.assertEqual(serializer.data["points"], 7)

    def test_standing_serializer_valid_payload(self):
        payload = {
            "championship": self.championship.id,
            "team": self.team.id,
            "played": 1,
            "wins": 1,
            "draws": 0,
            "losses": 0,
            "goals_for": 2,
            "goals_against": 1,
            "points": 3,
        }

        serializer = StandingSerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        standing = serializer.save()

        self.assertEqual(standing.points, 3)
        self.assertEqual(standing.goal_difference, 1)