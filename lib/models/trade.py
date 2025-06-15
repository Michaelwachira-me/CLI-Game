from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

# players can trade monsters, form connections/rival and compete
class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer(), primary_key=True)
    from_playerID = Column(Integer(), ForeignKey('players.id'))
    to_playerID = Column(Integer(), ForeignKey('players.id'))
    offered_monsters = Column(JSON)
    requested_monsters = Column(JSON)
    status = Column(String, default="pending")
    
    from_player = relationship("player", foreign_keys=[from_playerID])
    to_player = relationship("player", foreign_keys=[to_playerID])
   