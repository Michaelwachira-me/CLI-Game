from .base import Base
from sqlalchemy import Column, Integer, String

class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, unique=True)
   