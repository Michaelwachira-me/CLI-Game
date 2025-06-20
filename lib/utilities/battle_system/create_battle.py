from lib.models import Battle
from lib.db.connection import Session
from contextlib import contextmanager

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def create_battle(player1_id, player2_id, monster_teams, session) -> dict:
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