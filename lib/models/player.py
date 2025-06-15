
from sqlalchemy import Column, Integer, String, JSON 
from sqlalchemy.orm import relationship

from .base import Base

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, unique=True)

    level = Column(Integer(), default=1)
    insight = Column(Integer(), default=0)
    essence = Column(Integer(), default=0)
    achievements = Column(JSON, default=[]) 

    player_monsters = relationship("PlayerMonster", back_populates="player", cascade="all, delete-orphan")

    def __repr__(self):
        return (f"<Player(id={self.id}, name='{self.name}', level={self.level}, "
                f"insight={self.insight}, essence={self.essence})>")