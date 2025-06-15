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
        base_stats={"hp": fake.random_int(10, 100)},
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
achievements = []
for _ in range(4):
    achievement = Achievement(
        name=fake.unique.word().capitalize(),
        description=fake.sentence()
    )
    achievements.append(achievement)
session.add_all(achievements)
session.commit()

# give monsters to a player and have a progression
player_monsters = []
player_achievements = []
for player in players:
    playermonster = PlayerMonster(
        nickname=fake.unique.first_name(),
        level=fake.random_int(1, 5),
        expertise=fake.random_int(0, 100),
        current_stats={"hp": 50},
        species_id=fake.random_element(elements=species_collection).id,
        player_id=player.id
    )
    player_monsters.append(playermonster)

    playerAchievmt = Player_achievement(
        name=fake.word(), 
        player_id=player.id,
        achievement_id=fake.random_element(elements=achievements).id,
        progress=round(fake.pyfloat(0, 1), 2)
    )
    player_achievements.append(playerAchievmt)

session.add_all(player_monsters)
session.add_all(player_achievements)
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
trades_list = []
for _ in range(3):
    from_player, to_player = fake.random_elements(elements=players, length=2, unique=True)
    trade = Trade(
        from_playerID=from_player.id,
        to_playerID=to_player.id,
        offered_monsters=[fake.word() for _ in range(2)],
        requested_monsters=[fake.word() for _ in range(1)],
        status=fake.random_element(elements=('Pending', 'Accepted', 'Declined'))
    )
    trades_list.append(trade)

session.add_all(trades_list)

session.commit()
session.close()

print("Seeding done successfully!")

