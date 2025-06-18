from faker import Faker
from lib.db.connection import Session

from lib.models import Base, Player, Achievement, Player_achievement, MonsterSpecies, PlayerMonster, Trade, Battle

fake = Faker()
session = Session()

session.query(PlayerMonster).delete()
session.query(MonsterSpecies).delete()
session.query(Player).delete()
session.query(Player_achievement).delete()
session.query(Achievement).delete()
session.query(Battle).delete()
session.query(Trade).delete()

# Create species
species_collection = []
for _ in range(6):
    species = MonsterSpecies(
        name=fake.unique.word().capitalize(),
        element_type=fake.random_element(elements=('Fire', 'Water', 'Earth', 'Air')),
        base_stats={
            "hp": fake.random_int(30, 100),
            "attack": fake.random_int(5, 20),
            "defense": fake.random_int(5, 20)
        },
        rarity=fake.random_element(elements=('normal', 'rare', 'Elite', 'godslayer')),
        abilities=[fake.word() for _ in range(2)]
    )
    species_collection.append(species)
session.add_all(species_collection)
session.commit()

# create players
players = []
for _ in range(4):
    player = Player(
        username=fake.unique.user_name(),
        password=fake.password(),
        level=fake.random_int(1,5),
        experience=fake.random_int(0,500),
        money=round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
        achievements=[]
    )
    players.append(player)
session.add_all(players)
session.commit()

# create achievements
achievements = [
    Achievement(name="Spirit Whisperer", description="Holistically bonded with lost spirits."),
    Achievement(name="Corruption Cleanser", description="Prioritized cleansing exercise."),
    Achievement(name="Gaia Explorer", description="Explored all known regions."),
    Achievement(name="Master Tamer", description="Raise a spirit to new level.")
]

session.add_all(achievements)
session.commit()

# give monsters to a player and have a progression
player_monsters = []
player_achievements = []
for player in players:
    num_monsters = fake.random_int(1, 3)
    for _ in range(num_monsters):
        species = fake.random_element(elements=species_collection)
        playermonster = PlayerMonster(
            nickname=fake.unique.first_name(),
            level=fake.random_int(1, 5),
            experience=fake.random_int(0, 100),
            monster_species=species,
            player_id=player.id
        )
        session.add(playermonster)
        session.flush() # Flush so SQLAlchemy assigns IDs and relationships
        playermonster.initialize_current_stats() #uses species.base_stats
        player_monsters.append(playermonster)

    achievement = fake.random_element(elements=achievements)
    playerAchievmt = Player_achievement(
        name=achievement.name, 
        player_id=player.id,
        achievement_id=achievement.id,
        progress=round(fake.random_element(elements=[0.2, 0.5, 1.0]), 2)
    )
    session.add(playerAchievmt)
    player_achievements.append(playerAchievmt)

session.commit()

# create battles 
battles_list = []
for _ in range(3):
    p1, p2 = fake.random_elements(elements=players, length=2, unique=True)
    battle = Battle(
        player1_id=p1.id,
        player2_id=p2.id,
        result=fake.random_element(elements=('Player1 Win', 'Player2 Win', 'Draw')),
        battle_inventory={"items": [fake.word() for _ in range(2)]}
    )
    battles_list.append(battle)

session.add_all(battles_list)
session.commit()

# create trades
all_monsters = session.query(PlayerMonster).all()
trades_list = []
for _ in range(3):
    from_player, to_player = fake.random_elements(elements=players, length=2, unique=True)
    offered = [fake.random_element(elements=all_monsters).id for _ in range(1)]
    requested = [fake.random_element(elements=all_monsters).id for _ in range(1)]
    trade = Trade(
        from_playerID=from_player.id,
        to_playerID=to_player.id,
        offered_monsters=offered,
        requested_monsters=requested,
        status=fake.random_element(elements=('Pending', 'Accepted', 'Declined'))
    )
    trades_list.append(trade)

session.add_all(trades_list)

session.commit()
session.close()

print("Seeding done successfully!")

