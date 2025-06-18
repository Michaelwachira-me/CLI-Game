import typer
from lib.models import Player, MonsterSpecies, PlayerMonster
from lib.utilities.battle_system.create_battle import create_battle
from lib.utilities.battle_system.combat_system import execute_turn, calculate_battle_rewards
from lib.db.connection import Session
from sqlalchemy.sql import func

app = typer.Typer()
session = Session()

@app.command()
def start():
    """
    Cleanse a corrupted spirit by battling with your own monster.
    """

    try:
        player_id = 1  # TODO: in real game, get player dynamically
        player = session.query(Player).get(player_id)

        # Pick a random corrupted spirit species
        corrupted_spirit = session.query(MonsterSpecies).order_by(func.random()).first()

        typer.secho(f"\nA corrupted spirit appears: {corrupted_spirit.name} ({corrupted_spirit.element_type})!", fg=typer.colors.RED)

        # Get player's monsters, 
        # and initialize its current_stats if absent
        player_team = player.monsters
        for monster in player_team:
            if not monster.current_stats:
                 monster.initialize_current_stats()

        if not player_team:
            typer.echo("You have no monsters! Go explore Gaia first.")
            return

        typer.echo("\nChoose your monster for battle:")

        for index, monster in enumerate(player_team, start=1):
            typer.echo(f"{index}. {monster.nickname} (Level {monster.level}) HP: {monster.current_stats['hp']}")

        chosen_index = int(typer.prompt("Enter the number of your chosen monster")) - 1
        chosen_monster = player_team[chosen_index]
        
        # Reinitialize chosen_monster's current_stats freshly for this battle
        chosen_monster.initialize_current_stats()

        # Create battle (store only your monster's ID — spirit needs no DB)
        battle = create_battle(
            player1_id=player_id,
            player2_id=None,
            monster_teams={
                "player1": [chosen_monster.id],
                "corrupted": [corrupted_spirit.id]  # optional
            }
        )

        typer.echo("\nThe cleansing battle begins!")

        battle_id = battle["battle_id"]

        # Initialize corrupted spirit HP for this battle only
        corrupted_hp = corrupted_spirit.base_stats["hp"]

        turn = 1

        while corrupted_hp > 0 and chosen_monster.current_stats["hp"] > 0:
            typer.echo(f"\nTurn {turn}: {chosen_monster.nickname} vs corrupted {corrupted_spirit.name}")

            typer.echo("1. Spirit Strike")
            typer.echo("2. Guard")

            move_choice = int(typer.prompt("Choose your move"))

            if move_choice == 1:
                move = {"name": "Spirit Strike", "power": 2.0, "type_effectiveness": 1.0}
            else:
                move = {"name": "Guard", "power": 0.5, "type_effectiveness": 1.0}

            # Add temporary .current_stats to corrupted spirit
            corrupted_spirit.current_stats = {
                "attack": corrupted_spirit.base_stats["attack"],
                "defense": corrupted_spirit.base_stats["defense"],
                "hp": corrupted_hp
            }

            # Call turn
            result = execute_turn(battle_id, chosen_monster, corrupted_spirit, move)

            # Update local HP for next loop
            corrupted_hp = corrupted_spirit.current_stats["hp"]

            typer.echo(result["log"])

            turn += 1

        # Remove temp attribute (optional)
        if hasattr(corrupted_spirit, "current_stats"):
            del corrupted_spirit.current_stats

        # Decide winner
        if corrupted_hp <= 0:
            xp, money = calculate_battle_rewards(player_id, battle_difficulty=1)
            typer.echo(f"\nCleansing complete! You earned {xp} XP and {money} coins.")
        else:
            typer.echo("\nYou lost the cleansing battle. Heal your monster and try again!")

    except Exception as e:
        typer.echo(f"Error during cleansing: {e}")
