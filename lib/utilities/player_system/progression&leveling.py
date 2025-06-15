from lib.models import Player
from lib.db.connection import Session

session = Session()

def add_experience(player_id, xp):
    """
    add experience(xp) to the player's experience
    """
    player = session.query(Player).get(player_id)
    player.experience += xp
    session.commit()
    return player.experience

def level_up_player(player_id):
    """
    if needed, level up player:
        - define a threshold (eg. get 50xp per level)
        - as you level up, reward player with money
    """
    player = session.query(Player).get(player_id)
    needed_xp = player.level * 50
    
    leveled_up = False
    while player.experience >= needed_xp:
        player.experience -= needed_xp
        player.level += 1
        player.money += 50
        leveled_up = True
    
    session.commit()
    return {"level": player.level, "experience": player.experience, "money": player.money, "leveled_up": leveled_up}
        
    
    

