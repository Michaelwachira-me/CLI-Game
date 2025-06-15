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
    
    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="battles_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="battles_as_player2")
    
    
    def __repr__(self):
        return f"(Battle(id={self.id}, result={self.result}))"