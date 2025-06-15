# lib/db/seeker_manager.py
from sqlalchemy.exc import IntegrityError
from colorama import Fore, Style, init 
import json


init(autoreset=True) 

from lib.db.database import SessionLocal, init_db
from lib.models.player import Player
from lib.models.monster_species import MonsterSpecies

from typing import Optional

# --- Seeker Initiation and Attunement ---
def initiate_seeker(name: str) -> Optional[Player]:
    """
    Creates a new Seeker profile. Returns the Player object if successful, None otherwise.
    """
    db = SessionLocal()
    try:
        if not name or len(name.strip()) < 3:
            print(f"{Fore.RED}Name must be at least 3 characters long and not empty.{Style.RESET_ALL}")
            return None

        existing_player = db.query(Player).filter(Player.name == name).first()
        if existing_player:
            print(f"{Fore.YELLOW}A Seeker with the name '{name}' already exists. Please choose another.{Style.RESET_ALL}")
            return existing_player

        new_seeker = Player(name=name, level=1, insight=0, essence=0)
        db.add(new_seeker)
        db.commit()
        db.refresh(new_seeker)
        print(f"{Fore.GREEN}Welcome, Seeker {name}! Your journey to restore balance begins.{Style.RESET_ALL}")
        return new_seeker
    except IntegrityError:
        db.rollback()
        print(f"{Fore.RED}An unexpected error occurred during Seeker initiation (name conflict).{Style.RESET_ALL}")
        return None
    except Exception as e:
        db.rollback()
        print(f"{Fore.RED}An error occurred during Seeker initiation: {e}{Style.RESET_ALL}")
        return None
    finally:
        db.close()

def attune_to_realms(name: str) -> Optional[Player]:
    """
    Logs in an existing Seeker. Returns the Player object if successful, None otherwise.
    """
    db = SessionLocal()
    try:
        seeker = db.query(Player).filter(Player.name == name).first()
        if seeker:
            print(f"{Fore.CYAN}Seeker {name}, attuned to the realms. Welcome back!{Style.RESET_ALL}")
            return seeker
        else:
            print(f"{Fore.RED}Seeker '{name}' not found. Please check your name or initiate a new journey.{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}An error occurred during realm attunement: {e}{Style.RESET_ALL}")
        return None
    finally:
        db.close()

# --- Seeker Spiritual Growth ---
LEVEL_INSIGHT_REQUIREMENTS = {
    1: 0,
    2: 100,
    3: 250,
    4: 450,
    5: 700,
    6: 1000,
    7: 1350,
    8: 1750,
    9: 2200,
    10: 2700,
}

def gain_insight(seeker_id: int, amount: int) -> Optional[Player]:
    """
    Adds insight to a Seeker and checks for level-ups.
    Returns the updated Player object or None if seeker not found.
    """
    db = SessionLocal()
    try:
        seeker = db.query(Player).filter(Player.id == seeker_id).first()
        if not seeker:
            print(f"{Fore.RED}Seeker with ID {seeker_id} not found.{Style.RESET_ALL}")
            return None

        seeker.insight += amount
        print(f"{Fore.BLUE}{seeker.name} gained {amount} insight. Total insight: {seeker.insight}{Style.RESET_ALL}")

        while True:
            next_level_insight = LEVEL_INSIGHT_REQUIREMENTS.get(seeker.level + 1)
            if next_level_insight is None:
                print(f"{Fore.YELLOW}{seeker.name} is already at max Seeker level ({seeker.level}).{Style.RESET_ALL}")
                break

            if seeker.insight >= next_level_insight:
                seeker.level += 1
                seeker.insight -= next_level_insight
                print(f"{Fore.MAGENTA}Congratulations, {seeker.name}! You have reached Seeker Level {seeker.level}!{Style.RESET_ALL}")
            else:
                break

        db.commit()
        db.refresh(seeker)
        return seeker
    except Exception as e:
        db.rollback()
        print(f"{Fore.RED}An error occurred while gaining insight: {e}{Style.RESET_ALL}")
        return None
    finally:
        db.close()

# --- Seeker's Scroll Viewing ---
def view_seeker_scroll(seeker_id: int) -> Optional[dict]:
    """
    Retrieves and formats a Seeker's profile details.
    Returns a dictionary of seeker data or None if seeker not found.
    """
    db = SessionLocal()
    try:
        seeker = db.query(Player).filter(Player.id == seeker_id).first()
        if not seeker:
            print(f"{Fore.RED}Seeker with ID {seeker_id} not found.{Style.RESET_ALL}")
            return None

        # SQLAlchemy's JSON type handles conversion automatically.
        # seeker.achievements will already be a Python list/dict.
     
        parsed_achievements = seeker.achievements if seeker.achievements is not None else []

        profile_data = {
            "id": seeker.id,
            "username": seeker.name,
            "level": seeker.level,
            "insight": seeker.insight,
            "essence": seeker.essence,
            "milestone_recognition": parsed_achievements
        }
        return profile_data
    except Exception as e:
        print(f"{Fore.RED}An error occurred while viewing seeker scroll: {e}{Style.RESET_ALL}")
        return None
    finally:
        db.close()

# --- Local Testing Block (Run this file directly to test) ---
if __name__ == "__main__":
    init_db() # Ensure tables are created if not already

    print("\n--- Testing Seeker Initiation ---")
    seeker1 = initiate_seeker("Anya")
    seeker2 = initiate_seeker("Bolt")
    initiate_seeker("Anya") # Test existing player

    print("\n--- Testing Realm Attunement ---")
    current_seeker = attune_to_realms("Bolt")
    if current_seeker:
        print(f"Currently logged in as: {current_seeker.name}, Level {current_seeker.level}")
    else:
        print("Could not attune to realms.")
    attune_to_realms("NonExistentSeeker")

    print("\n--- Testing Gain Insight ---")
    if seeker1:
        print(f"\n{seeker1.name}'s initial level: {seeker1.level}, insight: {seeker1.insight}")
        gain_insight(seeker1.id, 50)
        gain_insight(seeker1.id, 60)
        gain_insight(seeker1.id, 200)

    print("\n--- Testing Seeker's Scroll ---")
    if current_seeker:
        bolt_profile = view_seeker_scroll(current_seeker.id)
        if bolt_profile:
            print(f"{Fore.LIGHTBLUE_EX}--- Seeker's Scroll for {bolt_profile['username']} ---{Style.RESET_ALL}")
            print(f"ID: {bolt_profile['id']}")
            print(f"Level: {bolt_profile['level']}")
            print(f"Insight: {bolt_profile['insight']}")
            print(f"Essence: {bolt_profile['essence']}")
            print(f"Milestone Recognition: {bolt_profile['milestone_recognition']}")
    view_seeker_scroll(999) # Test non-existent seeker