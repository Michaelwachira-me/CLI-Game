import random
from lib.models import Player, PlayerMonster, MonsterSpecies
from .catch_rate import calculate_catch_rate
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
        
def catch_monster(player_id, species_id, session) ->bool:
    """
    Helps check chance of catching monster using random chance+catch rate
        if monster is caught, CREATE new player_monster instance
        push base stats to player's current_stats
    """
    player = session.get(Player, player_id)
    species = session.get(MonsterSpecies, species_id)
        
    catch_probability = calculate_catch_rate(species.rarity, player.level)

    if random.random() <catch_probability:
            # ensure caught monster has a nickname to avoid NULL arising from player_monster's nickname constraint
            nickname = f"{species.name}_{random.randint(1000, 9999)}"
            caught_monster = PlayerMonster(
                nickname=nickname,
                player_id=player_id,
                species_id=species_id,
                level=1,
                experience=0,
                current_stats=species.base_stats.copy()
            )
            
            session.add(caught_monster)
            # session.commit()
            return True
    return False

def get_player_collection(player_id, session) -> list:
    """
    Given a player, how many monsters are owned by him?
    """
    collection = session.query(PlayerMonster).filter_by(player_id=player_id).all()
    return collection


        