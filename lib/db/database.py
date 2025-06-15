
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///gaia.db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


from lib.models.base import Base


def init_db():
    print("Attempting to initialize database...")
    # Import all models here so that Base can discover them
    # Note the relative import: models means models.py is in the same directory
    # If using multiple model files in a 'models' folder, you might import them like this:
    from lib.models import player, monster_species, achievement, battle, player_achievement, player_monster, trade 
    # Or, a simpler way that SQLAlchemy often handles is that once Base is imported,
    # and all your model classes (like Player, MonsterSpecies) inherit from Base,
    # Base.metadata.create_all() will discover them automatically, provided they are imported
    # *somewhere* in your application flow before init_db is called.
    # For testing, importing them explicitly here ensures discovery.

    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

def get_db():
    """
    This is a helper to get a database session when needed
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()