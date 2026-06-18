from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MatchEvent, Match
from apps.championships.services import recalculate_standings

@receiver(post_save, sender=MatchEvent)
def update_match_score(sender, instance, created, **kwargs):
    
    if not created:
        return
    
    if instance.event_type != MatchEvent.EventType.GOAL:
        return
    
    if not instance.team:
        return
    
    match = instance.match
    
    if instance.team_id == instance.match.home_team:
        instance.match.home_score += 1
    elif instance.team_id == instance.match.away_team:
        instance.match.away_score += 1

    match.save(update_fields=["home_score", "away_score"])   
        
@receiver
def update_standings_when_match_finished(sender, instance, **kwargs):
    if instance.status == Match.Status.FINISHED:
        recalculate_standings(instance.championship_id)