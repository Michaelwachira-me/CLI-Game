from lib.models import Trade, PlayerMonster
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

def propose_trade(from_player, to_player, offered_monsters, requested_monsters, session):
    """
    storing who sent, who receives, which monsters traded, and status
    """
    trade = Trade(
            from_playerID = from_player,
            to_playerID = to_player,
            offered_monsters=offered_monsters,
            requested_monsters=requested_monsters
    )
    session.add(trade)
    session.commit()
    return {
            "trade_id": trade.id,
            "status": trade.status
    }
    
def accept_or_decline_trade(trade_id, accept:bool, session):
    """
    Fetch trade via its ID:
        - if accepted trade, exchange the monster's owner
        - else, show declined
    """
    trade = session.query(Trade).get(trade_id)
        # validate existence and acceptance state
    if not trade or trade.status != "pending":
        return "Trade already processed or invalid trade"
        
    if accept:
            # change ownership
        for monster_id in trade.offered_monsters:
                monster = session.query(PlayerMonster).get(monster_id)
                monster.player_id = trade.to_playerID
            
        for monster_id in trade.requested_monsters:
                monster = session.query(PlayerMonster).get(monster_id)
                monster.player_id = trade.from_playerID
                
        trade.status = "accepted"
    else:
            trade.status = "declined"
    session.commit()
    return f"Trade {trade.status}"
                
        