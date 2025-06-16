from .base import Base
from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.orm import relationship

class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer(), primary_key=True)
    username = Column(String(), nullable=False, unique=True)
    password = Column(String(), nullable=False)
    level = Column(Integer(), default=1)
    experience = Column(Integer(), default=0)
    money = Column(Float(), default=0.0)
    achievements = Column(JSON, default=list)
    
    monsters = relationship("PlayerMonster", back_populates="player")
    battles_as_player1 = relationship("Battle", foreign_keys="Battle.player1_id", back_populates="player1")
    battles_as_player2 = relationship("Battle", foreign_keys="Battle.player2_id", back_populates="player2")

    
    def __repr__(self):
        return f"<Player: username={self.username}, level={self.level}, xp={self.experience}"
   
