from .base import Base
from sqlalchemy import Column, Integer, String

class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, unique=True)
   