from lib.db.connection import Session
from .stats_calc import calculate_stats_upon_leveling
from lib.models import PlayerMonster, MonsterSpecies
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
        
def level_up_monster(monster_id, session) -> dict:
    """
    feat: load monster, increase level plus recalculate stats based on level
    """
    monster = session.query(PlayerMonster).get(monster_id)
    monster_species = session.query(MonsterSpecies).get(monster.species_id)
        
    monster.level += 1
    monster.current_stats = calculate_stats_upon_leveling(
            monster_species.base_stats, monster.level
        )
        
        # session.commit()
    return {
            "level": monster.level,
            "current_stats": monster.current_stats
    }