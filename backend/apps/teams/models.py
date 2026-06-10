from django.conf import settings
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    shield = models.ImageField(upload_to='team_shields/', blank=True, null=True)
    
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="managed_teams",
        blank=True,
        null=True,
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Time"
        verbose_name_plural = "Times"
        
    def __str__(self):
        return self.name