
from sqlalchemy import Column, Integer, ForeignKey, String, JSON
from sqlalchemy.orm import relationship

from .base import Base

class PlayerMonster(Base):
    """
    Defaults on expertise and levels: Sets game rules
        - after catching monster, it will start at level 1
        - all monsters start with 0 XP and improve with training on battle
    Base stats in monsterspecies tell us the level that a monster starts with
        - so, in player_monsters, we will store in current_stats to track the stats' growth
        - so, stats are only affected on a player perspective.
    Cascade feat: for data integrity - ensuring that if a monster species
    no longer exists, then all playermonster entries are also removed.
    """
    __tablename__ = "player_monsters"

    id = Column(Integer(), primary_key=True)
    nickname = Column(String(), nullable=False, unique=True)
    level = Column(Integer(), default=1)
    expertise = Column(Integer(), default=0)
    current_stats = Column(JSON)

    species_id = Column(Integer(), ForeignKey("monster_species.id"), nullable=False)
    player_id = Column(Integer(), ForeignKey("players.id"), nullable=False)

    
    monster_species = relationship("MonsterSpecies", back_populates="player_monsters")
    

    # You will also need the relationship to Player
    # Assuming 'players' is the table name for the Player model
    player = relationship("Player", back_populates="player_monsters") # You'll need to define back_populates in Player model too

    def __repr__(self):
        return f"<PlayerMonster(id={self.id}, nickname='{self.nickname}', level={self.level}, species_id={self.species_id}, player_id={self.player_id})>"