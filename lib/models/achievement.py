from .base import Base
from sqlalchemy import Column, Integer, String, Text

class Achievement(Base):
    __tablename__ = 'achievements'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, unique=True)
    description = Column(Text, nullable=True)
   