
from lib.db.database import init_db, SessionLocal
from lib.models.player import Player
from lib.models.monster_species import MonsterSpecies

def seed_database():
    db = SessionLocal()
    try:
        print("Seeding database...")

        
        db.query(Player).delete()
        db.query(MonsterSpecies).delete()
        db.commit()
        print("Cleared existing Player and MonsterSpecies data.")

        # Create some initial MonsterSpecies with CORRECT arguments
        # base_stats is now a dictionary for the JSON column
        # 'element' is now 'element_type'
        species1 = MonsterSpecies(
            name="Goblin",
            element_type="Earth", 
            base_stats={"hp": 50, "attack": 10, "defense": 5},
            rarity="Common",
            abilities=["Stomp", "Growl"]
        )
        species2 = MonsterSpecies(
            name="Dragon Pup",
            element_type="Fire", 
            base_stats={"hp": 80, "attack": 15, "defense": 8}, 
            rarity="Rare",
            abilities=["Fire Breath", "Tail Whip"]
        )
        species3 = MonsterSpecies(
            name="Slime",
            element_type="Water",
            base_stats={"hp": 30, "attack": 5, "defense": 3}, 
            rarity="Common",
            abilities=["Ooze", "Absorb"]
        )

        db.add_all([species1, species2, species3])
        db.commit()
        print("Seeded initial monster species.")

        print("Database seeding complete.")

    except Exception as e:
        db.rollback()
        print(f"An error occurred during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db() # Ensure tables are created first
    seed_database()