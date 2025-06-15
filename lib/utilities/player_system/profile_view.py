from lib.models import Player
from lib.db.connection import Session

session = Session()

def get_player_profile(player_id):
    """
    fetch player's stats via ID
    return a dictionary with profile
    """
    player = session.query(Player).get(player_id)
    return {
        "username": player.username,
        "level": player.level,
        "experience": player.experience,
        "money": player.money,
        "achievements": player.achievements
    }