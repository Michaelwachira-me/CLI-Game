from .base import Base
from sqlalchemy import Column, Integer, String

class Battle(Base):
    __tablename__ = 'battles'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, unique=True)
   