from django.db import models
from apps.teams.models import Team


class Player(models.Model):
    class Position(models.TextChoices):
        GOALKEEPER = "GOALKEEPER", "Goleiro"
        DEFENDER = "DEFENDER", "Defensor"
        MIDFIELDER = "MIDFIELDER", "Meio-campo"
        FORWARD = "FORWARD", "Atacante"

    name = models.CharField(max_length=120)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    position = models.CharField(
        max_length=20,
        choices=Position.choices,
        blank=True,
        null=True,
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="players",
        blank=True,
        null=True,
    )

    photo = models.ImageField(upload_to="players/photos/", blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Jogador"
        verbose_name_plural = "Jogadores"

    def __str__(self):
        return self.nickname or self.name