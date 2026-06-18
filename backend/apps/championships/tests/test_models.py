from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from apps.championships.models import Championship, Standing
from apps.teams.models import Team

class ChampionshipModelTests(TestCase):
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
        
    def test_create_championship(self):
        championship = Championship.objects.create(
            name="Campeonato Teste",
            season="2026",
            city="Pau dos Ferros",
            modality=Championship.Modality.FOOTBALL,
            format=Championship.Format.LEAGUE,
        )
        championship.teams.add(self.team)
        
        self.assertEqual(str(championship), "Campeonato Teste - 2026")
        self.assertEqual(championship.team.count(), 1)
        self.assertEqual(championship.is_active)
        
    def test_create_standing(self):
        championship = Championship.objects.create(
            name="Campeonato Teste",
            season="20260",
            city="Pau dos Ferros",
            modality=Championship.Modality.FOOTBALL,
            format=Championship.Format.LEAGUE,
        )
        
        standing = Standing.objects.create(
            championship=championship,
            team=self.team,
            goals_for=5,
            goals_against=2,
            points=10,
        )
        
        self.assertEqual(standing.goal_difference, 3)
        self.assertEqual(str(standing), "Arena FC - 10 pts")
        
    def test_unique_standing_per_championship_and_team(self):
        championship = Championship.objects.create(
            name="Campeonato Teste",
            season="2026",
            city="Pau dos Ferros",
            format=Championship.Format.LEAGUE,
        )
        
        Standing.objects.create(
            championship=championship,
            team=self.team,
        )
        
        with self.assertRaises(IntegrityError):
            Standing.objects.create(
                championship=championship,
                team=self.team,
            )