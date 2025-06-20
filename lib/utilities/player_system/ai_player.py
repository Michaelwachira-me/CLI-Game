from lib.models import Player
from lib.db.connection import Session

# # Create an AI player ONCE
# session = Session()
# ai_player = Player(
#     username="AI_OPPONENT",
#     password="",
#     level=1,
#     experience=0,
#     money=0,
#     achievements=[]
# )
# session.add(ai_player)
# session.commit()
# print(f"AI Player created with ID: {ai_player.id}")
# session.close()

def get_or_create_ai_player(session):
    ai_player = session.query(Player).filter_by(username="AI_OPPONENT").first()
    if not ai_player:
        ai_player = Player(
            username="AI_OPPONENT",
            password="",
            level=1,
            experience=0,
            money=0,
            achievements=[]
        )
        session.add(ai_player)
        session.commit()
    return ai_player

