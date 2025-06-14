from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models.base import Base

engine = create_engine("sqlite:///gaia.db")
Session = sessionmaker(bind=engine)