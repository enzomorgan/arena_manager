from django.db import models
from apps.teams.models import Team

class Championship(models.Model):
    class Modality(models.TextChoices):
        FOOTBALL = 'FOOTBALL', 'Futebol'
        BASKETBALL = 'BASKETBALL', 'Basquete'
        VOLLEYBALL = 'VOLLEYBALL', 'Vôlei'
        SOCIETY = 'SOCIETY', 'Society'
        FUTSAL = 'FUTSAL', 'Futsal'
        
    class Format(models.TextChoices):
        LEAGUE = "LEAGUE", "Pontos Corridos"
        GROUPS = "GROUPS", "Fase de Grupos"
        KNOCKOUT = "KNOCKOUT", "Mata-Mata"
        
    name = models.CharField(max_length=255)
    season = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    
    modality = models.CharField(
        max_length=20,
        choices=Modality.choices,
    )
    
    format = models.CharField(
        max_length=20,
        choices=Format.choices,
    )
    
    teams = models.ManyToManyField(
        Team, 
        related_name="championships",
        blank=True,
    )
    
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Campeonato"
        verbose_name_plural = "Campeonatos"
        
    def __str__(self):
        return f"{self.name} - {self.season}"
    
class Standing(models.Model):
    championship = models.ForeignKey(
        Championship,
        on_delete=models.CASCADE,
        related_name="standings",
    )
    
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.CASCADE,
    )
    
    played = models.PositiveIntegerField(default=0)
    
    wins = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    
    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    
    points = models.PositiveIntegerField(default=0)
    
    class Meta: 
        unique_together = (
            "championship",
            "team",
        )
        
    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against
    
    def __str__(self):
        return f"{self.team} - {self.points} pts"