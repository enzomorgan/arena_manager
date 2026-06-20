from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.teams.models import Team


class TeamPermissionTests(APITestCase):
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

    def test_unauthenticated_user_cannot_list_teams(self):
        response = self.client.get("/api/teams/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_create_team(self):
        response = self.client.post(
            "/api/teams/",
            {
                "name": "Bola FC",
                "city": "Mossoró",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Team.objects.count(), 1)

    def test_unauthenticated_user_cannot_update_team(self):
        response = self.client.patch(
            f"/api/teams/{self.team.id}/",
            {
                "name": "Nome Alterado",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.team.refresh_from_db()
        self.assertEqual(self.team.name, "Arena FC")

    def test_unauthenticated_user_cannot_delete_team(self):
        response = self.client.delete(f"/api/teams/{self.team.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Team.objects.count(), 1)