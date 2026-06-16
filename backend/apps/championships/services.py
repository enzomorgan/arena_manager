from apps.championships.models import Championship, Standing
from apps.matches.models import Match
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
    
    
def generate_round_robin(championship):
    teams = list(championship.teams.all())
    
    if len(teams) < 2:
        raise ValueError(
            "O campeonato precisa ter pelo menos 2 times."
        )
        
    if len(teams) % 2:
        teams.append(None)
        
    rounds = len(teams) - 1
    halg = len(teams) // 2
    
    for round_number in range(rounds):
        
        left = teams[:half]
        right = teams[half:]
        right.reverse()
        
        for home, away in zip(left, right):
            
            if home is None or away is None:
                continue
            
            Match.objects.create(
                championship=championship,
                home_team=home,
                away_team=away,
                round_number=round_number + 1,
            )
            
        teams = (
            [teams[0]]
            + [teams[-1]]
            + teams[1:-1]
        )