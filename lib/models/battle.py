from .base import Base
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

class Battle(Base):
    """
    battle between two parties:
        - player 2 can be NULL is AI is playing
    result defines winner
        - either player1, player2, or draw
    """
    __tablename__ = 'battles'
    
    id = Column(Integer(), primary_key=True)
    player1_id = Column(Integer(), ForeignKey("players.id"))
    player2_id = Column(Integer(), ForeignKey("players.id"), nullable=True)
    result = Column(String)
    battle_inventory = Column(JSON, default=list)
    
    player1 = relationship("player", foreign_keys=[player1_id])
    player2 = relationship("player", foreign_keys=[player2_id])
    
    def __repr__(self):
        return f"(Battle(id={self.id}, result={self.result}))"