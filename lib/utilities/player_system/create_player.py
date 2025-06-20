from lib.models import Player
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

def create_player(username, password, session):
    # validate if username exists
        existing_username = session.query(Player).filter_by(username=username).first()
        if existing_username:
            raise ValueError("This username is taken!")
        
        # create new Player instance
        new_player = Player(
            username=username,
            password=password,
            level=1,
            experience=0,
            money=200.0,
            achievements=[]
        )
        session.add(new_player)
        session.commit()
        
        return new_player

# Look up player by username and validate password
def login_player(username,password, session):
        player = session.query(Player).filter_by(username=username).first()
        if player and player.password == password:
            return player
        else:
            raise ValueError("Invalid password or username")
        