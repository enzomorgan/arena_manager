from django.contrib.auth import get_user_model
from django.test import TestCase
from apps.players.models import Player
from apps.teams.models import Team

class PlayerModelTest(TestCase):
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
        
    def test_create_player(self):
        player = Player.objects.create(
            name="João",
            nickname="J",
            position=Player.Position.FORWARD,
            team=self.team,
        )
        
        self.assertEqual(player.name, "João")
        self.assertEqual(player.team, self.team)
        
    def test_update_player(self):
        player = Player.objects.create(
            name="João",
            nickname="J",
            position=Player.Position.FORWARD,
            team=self.team,
        )
        
        player.nickname = "Joãozinho"
        player.save()
        
        player.refresh_from_db()
        
        self.assertEqual(
            player.nickname,
            "Joãozinho",
        )
        
    def test_delete_player(self):
        player = Player.objects.create(
            name="João",
            nickname="J",
            position=Player.Position.FORWARD,
            team=self.team,
        )
        
        player.delete()
        
        self.assertEqual(
            Player.objects.count(),
            0,
        )