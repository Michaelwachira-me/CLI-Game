from lib.db.connection import Session
from .stats_calc import calculate_stats_upon_leveling
from lib.models import PlayerMonster

session = Session()
def level_up_monster(monster_id) -> dict:
    """
    feat: load monster, increase level plus recalculate stats based on level
    """
    monster = session.query(PlayerMonster).get(monster_id)
    monster.level += 1
    monster.current_stats = calculate_stats_upon_leveling(
        monster.species.base_stats, monster.level
    )
    
    session.commit()
    return monster.current_stats