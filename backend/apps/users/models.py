from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        ORGANIZER = "ORGANIZER", "Organizador"
        REFEREE = "REFEREE", "Árbitro"
        TEAM_MANAGER = "TEAM_MANAGER", "Representante"
        
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.TEAM_MANAGER,
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return self.username