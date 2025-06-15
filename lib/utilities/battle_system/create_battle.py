from lib.models import Battle
from lib.db.connection import Session

session = Session()

def create_battle(player1_id, player2_id, monster_teams) -> dict:
    """
    Defines who's fighting and using which monsters
    """
    battle = Battle(
        player1_id=player1_id,
        player2_id=player2_id,
        result = None,
        battle_log=[{"monster_teams": monster_teams}]
    )
    
    session.add(battle)
    session.commit()
    
    return {
        "battle_id": battle.id,
        "player1_id": player1_id,
        "player2_id": player2_id,
        "monster_teams": monster_teams
    }


    
