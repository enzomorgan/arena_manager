from django.contrib.auth import get_user_model
from django.test import TestCase
from apps.teams.models import Team
from apps.teams.serializers import TeamSerializer

class TeamSerializerTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="123456",
        )
        
    def test_team_serializer_returns_expected_fields(self):
        team = Team.objects.create(
            name="Arena FC",
            city="Pau dos Ferros",
            founded_year=2020,
            manager=self.user,
        )
        
        serializer = TeamSerializer(team)
        
        self.assertIn("id", serializer.data)
        self.assertIn("name", serializer.data)
        self.assertIn("city", serializer.data)
        self.assertIn("founded_year", serializer.data)
        self.assertIn("shield", serializer.data)
        self.assertIn("manager", serializer.data)
        self.assertIn("created_at", serializer.data)
        
        self.assertEqual(serializer.data["name"], "Arena FC")
        self.assertEqual(serializer.data["city"], "Pau dos Ferros")
        self.assertEqual(serializer.data["founded_year"], 2020)
        self.assertEqual(serializer.data["manager"], self.user.id)
        
    def test_team_serializer_valid_payload(self):
        payload = {
            "name": "Bola FC",
            "city": "Mossoró",
            "founded_year": 2021,
            "manager": self.user.id,
        }
        
        serializer = TeamSerializer(data=payload)
        
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        team = serializer.save()
        
        self.assertEqual(team.name, "Bola FC")
        self.assertEqual(team.city, "Mossoró")
        self.assertEqual(team.manager, self.user)
        
    def test_team_serializer_requires_name(self):
        payload = {
            "city": "Mossoró",
            "founded_year": 2021,
            "manager": self.user.id,
        }

        serializer = TeamSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_team_serializer_requires_city(self):
        payload = {
            "name": "Bola FC",
            "founded_year": 2021,
            "manager": self.user.id,
        }

        serializer = TeamSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
        self.assertIn("city", serializer.errors)