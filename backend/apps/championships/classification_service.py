from apps.championships.models import Standing
from apps.matches.models import Match

def recalculate_standings(championship):
    Standing.objects.filter(
        championship=championship
    ).delete()
    
    teams = championship.teams.all()
    
    standings = {}
    
    for team in teams:
        
        standings[team.id] = Standing.objects.create(
            championship=championship,
            team=team,
        )
        
    matches = Match.objects.filter(
        championship=championship,
        status=Match.Status.FINISHED,
    )
    
    for match in matches:
        
        home = standings[match.home_team.id]
        away = standings[match.away_team.id]
        
        home.played += 1
        away.played += 1
        
        home.goals_for += match.home_score
        home.goals_against += match.away_score
        
        away.goals_for += match.away_score
        away.goals_against += match.home_score
        
        if match.home_score > match.away_score:
            
            home.wins += 1
            home.points += 3
            
            away.losses += 1
            
        elif match.home_score < match.away_score:
            
            away.wins += 1
            away.points += 3
            
            home.losses += 1
            
        else:
            
            home.draws += 1
            away.draws += 1
            
            home.points += 1
            away.points += 1
            
    for standing in standings.values():
        standing.save()