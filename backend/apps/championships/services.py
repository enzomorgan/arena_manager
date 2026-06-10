from apps.championships.models import Championship, Standing
from apps.matches.models import Match

def recalculate_standings(championship_id):
    championship = Championship.objects.get(id=championship_id)
    
    Standing.objects.filter(championship=championship).delete()
    
    for team in championship.teams.all():
        Standing.objects.create(
            championship=championship,
            team=team,
        )
        
    finished_matches = Match.objects.filter(
        championship=championship,
        status=Match.Status.FINISHED,
    )
    
    for match in finished_matches:
        home_standing = Standing.objects.get(
            championship=championship,
            team=match.home_team,
        )
        
        away_standing = Standing.objects.get(
            championship=championship,
            team=match.away_team,
        )
        
        home_standing.played += 1
        away_standing.played += 1
        
        home_standing.gols_for += match.home_score
        home_standing.goals_against += match.away_score

        away_standing.goals_for += match.away_score
        away_standing.goals_against += match.home_score
        
        if match.home_score > match.away_score:
            home_standing.wins += 1
            home_standing.points += 3

            away_standing.losses += 1

        elif match.home_score < match.away_score:
            away_standing.wins += 1
            away_standing.points += 3

            home_standing.losses += 1

        else:
            home_standing.draws += 1
            away_standing.draws += 1

            home_standing.points += 1
            away_standing.points += 1

        
        home_standing.save()
        away_standing.save()
        
    return Standing.objects.filter(
        championship=championship,
    ).order_by(
        "-points",
        "-wins",
        "-goals_for",
    )