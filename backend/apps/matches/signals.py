from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Match, MatchEvent
from apps.championships.services import recalculate_standings

@receiver(post_save, sender=MatchEvent)
def update_match_score(sender, instance, created, **kwargs):
    
    if not created:
        return
    
    if instance.event_type != MatchEvent.EventType.GOAL:
        return
    
    if instance.team_id is None:
        return
    
    match = instance.match
    
    if instance.team_id == match.home_team_id:
        match.home_score += 1
    elif instance.team_id == match.away_team_id:
        match.away_score += 1
    else:
        return

    match.save(update_fields=["home_score", "away_score"])   
        
@receiver(post_save, sender=Match)
def update_standings_when_match_finished(sender, instance, **kwargs):
    if instance.status == Match.Status.FINISHED:
        recalculate_standings(instance.championship_id)