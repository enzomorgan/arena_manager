from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.teams.models import Team

class TeamAPIViewTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="123456",
        )
        
        self.client.force_authenticate(self.user)
        
    def test_create_team(self):
        response = self.client.post(
            "/api/teams/",
            {
                "name": "Arena FC",
                "city": "Pau dos Ferros",
            },
            format="json",
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
        
    def test_list_teams(self):
        Team.objects.create(
            name="Arena FC",
            city="Pau dos Ferros",
            manager=self.user,
        )

        response = self.client.get("/api/teams/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)