from django.db import models
from apps.championships.models import Championship
from apps.teams.models import Team

class Match(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Agendada"
        IN_PROGRESS = "IN_PROGRESS", "Em andamento"
        FINISHED = "FINISHED", "Finalizada"
        CANCELED = "CANCELED", "Cancelada"
        
    championship = models.ForeignKey(
        Championship,
        on_delete=models.CASCADE,
        related_name="matches",
    )
    
    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="home_matches",
    )
    
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="away_matches",
    )
    
    date = models.DateTimeField()
    round_number = models.PositiveIntegerField(default=1)
    
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["date"]
        verbose_name = "Partida"
        verbose_name_plural = "Partidas"
        
    def __str__(self):
        return f"{self.home_team} x {self.away_team}"
    
class MatchEvent(models.Model):
    class EventType(models.TextChoices):
        GOAL = "GOAL", "Gol"
        ASSIST = "ASSIST", "Assistência"
        YELLOW_CARD = "YELLOW_CARD", "Cartão Amarelo"
        RED_CARD = "RED_CARD", "Cartão Vermelho"
        
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name="events",
    )
    
    player = models.ForeignKey(
        "players.Player",
        on_delete=models.CASCADE,
    )
    
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
    )
    
    event_type = models.CharField(
        max_length=20,
        choices=EventType.choices,
    )
    
    minute = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )