from lib.models import Battle, Player
from lib.utilities.monster_system.name_getter import get_monster_name
from lib.db.connection import Session
import random
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

def calculate_damage(attacker_stats:dict, defender_stats:dict, move_power, type_effectiveness) -> int:
    """
    Defines how much damage the attacker causes on the defending monster
    - considers: attacker and defenders' stats; 
        - move's base power and its effectiveness (ie. 1.0 for lesseffective)
    - returns an integer value for damage dealt.
    """
    
    attack = attacker_stats['attack']
    defense = defender_stats['defense']
    
    # find base difference
    base_damage = attack - defense
    
    # Ensure base damage is 1 to protect against negative damage
    if base_damage < 1:
        base_damage = 1
    
    total_damage = base_damage * move_power * type_effectiveness
    
    # input randomness so that damage slightly differs like in pokemon
    random_value = random.uniform(0.7, 1.0)
    total_damage = total_damage * random_value
    
    return int(total_damage)

def execute_turn(battle_id, attacker_monster, defender_monster, move, session) -> dict:
    """
    attacker_monster and defender_monster are ORM objects:
        - so, extracts stats into dicts, then calls calculate_damage
    - PlayerMonster has .current_stats
    - MonsterSpecies has .base_stats
    """

    # Get attacker stats
    if hasattr(attacker_monster, "current_stats"):
        attacker_stats = {
            "name": get_monster_name(attacker_monster),
            "attack": attacker_monster.current_stats["attack"],
            "defense": attacker_monster.current_stats["defense"],
            "current_hp": attacker_monster.current_stats["hp"]
        }
    else:
        attacker_stats = {
            "name": get_monster_name(attacker_monster),
            "attack": attacker_monster.base_stats["attack"],
            "defense": attacker_monster.base_stats["defense"],
            "current_hp": attacker_monster.base_stats["hp"]
        }

    # Extract defender stats
    if hasattr(defender_monster, "current_stats"):
        defender_stats = {
            "name": get_monster_name(defender_monster),
            "attack": defender_monster.current_stats["attack"],
            "defense": defender_monster.current_stats["defense"],
            "current_hp": defender_monster.current_stats["hp"]
        }
    else:
        defender_stats = {
            "name": get_monster_name(defender_monster),
            "attack": defender_monster.base_stats["attack"],
            "defense": defender_monster.base_stats["defense"],
            "current_hp": defender_monster.base_stats["hp"]
        }


    # Calculate damage
    damage = calculate_damage(
        attacker_stats,
        defender_stats,
        move['power'],
        move['type_effectiveness']
    )

    # Subtract HP in local stats
    defender_stats['current_hp'] -= damage
    if defender_stats['current_hp'] < 0:
        defender_stats['current_hp'] = 0

    # Update above stats to ORM object
    if hasattr(defender_monster, "current_stats"):
        defender_monster.current_stats["hp"] = defender_stats['current_hp']
    else:
        # MonsterSpecies doesn't store HP in DB
        pass

    
    # Log turn in Battle
    battle = session.query(Battle).get(battle_id)
    battle.battle_inventory.append({
            "turn": {
                "attacker": attacker_stats['name'],
                "defender": defender_stats['name'],
                "move": move['name'],
                "damage": damage,
                "defender_hp": defender_stats['current_hp']
            }
        })
    # session.commit()

    return {
            "damage": damage,
            "defender_hp": defender_stats['current_hp'],
            "log": f"{attacker_stats['name']} used {move['name']} and dealt {damage} damage! "
                f"{defender_stats['name']} has {defender_stats['current_hp']} HP left."
    }
   
def check_battle_end(battle_id, session) -> bool:
    """
    Check if the battle should end — for example, if all monsters 
    on a player's team have died (HP ≤ 0).
    """
    battle = session.query(Battle).get(battle_id)
    
        # use the last monster situation 
    last_battle_turn = battle.battle_inventory[-1]
    monster_teams = last_battle_turn['monster_teams']

        # check each player in teams
    for player in monster_teams:
        monsters = monster_teams[player]
            
            # how many monsters are gone?
        fallen_monsters = 0
            
        for monster in monsters:
            if monster['current_hp'] <= 0:
                    fallen_monsters +=1
                    
            # if all are fallen, end battle, else continue
            if fallen_monsters == len(monsters):
                return True
        return False

def apply_status_effects(monster_id, effect_type):
    # In the future, we can other logic to keep the game interesting
    pass


def calculate_battle_rewards(winner_id, battle_difficulty, session) -> tuple:
    """
    reward system to show better monsters in harder battles
    """
    xp = 70 * battle_difficulty
    money = 35 * battle_difficulty
    player = session.query(Player).get(winner_id)
    player.experience += xp
    player.money += money
        
    # session.commit()
    return xp, money
    