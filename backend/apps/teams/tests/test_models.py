from django.contrib.auth import get_user_model
from django.test import TestCase
from apps.teams.models import Team

class TeamModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="123456",
        )
        
    def test_create_team(self):
        team = Team.objects.create(
            name="Arena FC",
            city="Pau dos Ferros",
            manager=self.user,
        )
        
        self.assertEqual(team.name, "Arena FC")
        self.assertEqual(team.city, "Pau dos Ferros")
        
    def test_update_team(self):
        team = Team.objects.create(
            name="Arena FC",
            city="Pau dos Ferros",
            manager=self.user,
        )
        
        team.name = "Arena Manager FC"
        team.save()

        team.refresh_from_db()

        self.assertEqual(
            team.name,
            "Arena Manager FC",
        )
        
    def test_delete_team(self):
        team = Team.objects.create(
            name="Arena FC",
            city="Pau dos Ferros",
            manager=self.user,
        )

        team.delete()

        self.assertEqual(
            Team.objects.count(),
            0,
        )