from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship

from .base import Base

class MonsterSpecies(Base):
    """
    1. Why use JSON instead of columsn on base_stats, abilities? 
        - To achieve one of the bonus challenges.
    2. base_stats is like: {"hp": 40, "attack": 55, "defence": 50}
    3. rarity implies a monster being like: common, rare, legendary
    4. the abilities on JSON can be in an array: ["fireBlast", "wavy"]
    """
    __tablename__ = "monster_species"
    
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, unique=True)
    element_type = Column(String(), nullable=False)
    base_stats = Column(JSON)
    rarity = Column(String())
    abilities = Column(JSON)
    
    player_monsters = relationship("PlayerMonster", back_populates="monster_species", cascade="all, delete-orphan")