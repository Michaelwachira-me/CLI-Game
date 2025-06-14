from .base import Base
from sqlalchemy import Column, Integer, String

class Player_achievement(Base):
    __tablename__ = 'player_achievements'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, unique=True)
   