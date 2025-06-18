from lib.models import Battle
from lib.db.connection import Session

session = Session()

def create_battle(player1_id, player2_id, monster_teams) -> dict:
    """
    Defines who's fighting and using which monsters
    - Accepts monster_teams as [[Monster objects]]
    - Stores monster_teams as dict.
    """
    battle = Battle(
        player1_id=player1_id,
        player2_id=player2_id,
        result=None,
        battle_inventory=[{"monster_teams": monster_teams}]
    )

    session.add(battle)
    session.commit()

    return {
        "battle_id": battle.id,
        "monster_teams": monster_teams
    }