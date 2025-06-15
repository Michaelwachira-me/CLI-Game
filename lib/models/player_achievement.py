from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float

class Player_achievement(Base):
    __tablename__ = 'player_achievements'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, unique=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    achievement_id = Column(Integer, ForeignKey('achievements.id'))
    progress = Column(Float, default=0.0)
   