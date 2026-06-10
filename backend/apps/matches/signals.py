from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MatchEvent, Match
from apps.championships.services import recalculate_standings

@receiver(post_save, sender=MatchEvent)
def update_match_score(sender, instace, created, **kwargs):
    
    if not created:
        return
    
    if instace.event_type != "GOAL":
        return
    
    match = instace.match
    
    if instace.team == match.home_team:
        match.home_score += 1
    else:
        match.away_score += 1
        
    match.save()
    
@receiver
def update_standings_when_match_finished(sender, instance, **kwargs):
    if instance.status == Match.Status.FINISHED:
        recalculate_standings(instance.championship_id)