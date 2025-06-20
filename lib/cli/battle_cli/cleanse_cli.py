import typer
import time
import random
from contextlib import contextmanager
from lib.models import Player, MonsterSpecies, PlayerMonster
from lib.utilities.battle_system.create_battle import create_battle
from lib.utilities.battle_system.combat_system import execute_turn, calculate_battle_rewards
from lib.utilities.battle_system.battle_ui import display_turn, your_move_prompt, show_move_result, show_separator
from lib.utilities.player_system.create_player import login_player
from lib.utilities.player_system.ai_player import get_or_create_ai_player
from lib.db.connection import Session
from sqlalchemy.sql import func
from lib.utilities.clear_screen import clear_screen

app = typer.Typer()

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        
@app.command()
def start():
    """
    Cleanse a corrupted spirit by battling with your own monster.
    """
    # typer.echo("\n--- Corrupted Grove: Where Shadows Linger ---")
    # time.sleep(1)
    
    try:
        with get_session() as session:
            # Login for player
            typer.secho("\n=== LOGIN ===", fg=typer.colors.CYAN, bold=True)
            username = typer.prompt("Your username")
            password = typer.prompt("Your password", hide_input=True)

            player = login_player(username, password, session)
            ai_player = get_or_create_ai_player(session)
            clear_screen()
            
            # game narrative to improve UI
            typer.secho(f"\nWelcome, {player.username}. Your inner harmony radiates at level {player.level}.", fg=typer.colors.BLUE) 
            time.sleep(1)
            
            typer.echo("\nDark winds twist the grove around you...")
            time.sleep(1.5)

            # Pick a random corrupted spirit species
            corrupted_spirit = session.query(MonsterSpecies).order_by(func.random()).first()

            typer.secho(f"\nA corrupted spirit appears: {corrupted_spirit.name} ({corrupted_spirit.element_type})!", fg=typer.colors.BLACK, bold=True)
            time.sleep(1)
            
            typer.secho("\nThrough cleansing, you release its pain — restoring your harmony and the grove's purity.", fg=typer.colors.BRIGHT_BLACK, bold=True)
            time.sleep(1)
            # Get player's monsters, 
            # and initialize its current_stats if absent
            player_team = player.monsters
            for monster in player_team:
                if not monster.current_stats:
                    monster.initialize_current_stats()

            if not player_team:
                typer.secho("You have no monsters! Go explore Gaia first.", fg=typer.colors.YELLOW)
                return

            typer.secho("\nChoose your monster for battle:", fg=typer.colors.BRIGHT_BLACK, bold=True)

            for index, monster in enumerate(player_team, start=1):
                typer.echo(f"{index}. {monster.nickname} (Level {monster.level}) HP: {monster.current_stats['hp']}")

            chosen_index = int(typer.prompt("Enter the number of your chosen monster")) - 1
            chosen_monster = player_team[chosen_index]
            
            # Reinitialize chosen_monster's current_stats freshly for this battle
            chosen_monster.initialize_current_stats()
            time.sleep(1.5)

            # Create battle (store only your monster's ID — spirit needs no DB)
            battle = create_battle(
                player1_id=player.id,
                player2_id=ai_player.id,
                monster_teams={
                    "player1": [chosen_monster.id],
                    "player2": [corrupted_spirit.id]
                },
                session=session
            )

            typer.secho("\n===The cleansing battle begins!===", fg=typer.colors.BRIGHT_BLACK, bold=True,)

            battle_id = battle["battle_id"]

            # Initialize corrupted spirit HP for this battle only
            corrupted_hp = corrupted_spirit.base_stats["hp"]

            turn = 1

            while corrupted_hp > 0 and chosen_monster.current_stats["hp"] > 0:
                show_separator()
                display_turn(
                    chosen_monster.nickname, 
                    chosen_monster.current_stats["hp"],
                    f"Corrupted {corrupted_spirit.name}",
                    corrupted_hp
                )
                
                move_choice = your_move_prompt()
                    # Since move_choices are 3 -> Attack, Defend, Surrender
                        # Handle the case where the player surrenders:
                if move_choice == 3:
                    typer.secho("\n You fled the battle. The corruption persists...", fg=typer.colors.RED, bold=True)
                    typer.secho("Returning to Battle Menu...", fg=typer.colors.BRIGHT_BLUE)
                    return
                
                # otherwise, if player chooses Attack or Defend, pick move:
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

                # Player moves on corrupted spirit
                # Call turn
                result = execute_turn(battle_id, chosen_monster, corrupted_spirit, move, session)

                # Update local HP for next loop
                corrupted_hp = corrupted_spirit.current_stats["hp"]
                show_move_result(
                    chosen_monster.nickname, 
                    f"Corrupted {corrupted_spirit.name}", 
                    move["name"], result["damage"], corrupted_hp)
                
                # If corrupted spirit fainted, skip counterattack
                if corrupted_hp <= 0:
                    break
                
                show_separator()
                # Now corrupted spirit counterattacks!
                typer.secho(f" Corrupted Spirit's Move:", fg=typer.colors.BRIGHT_RED, bold=True)
                spirit_moves = [
                        {"name": "Corrupted Blast", "power": 1.5, "type_effectiveness": 1.0},
                        {"name": "Dark Mist", "power": 1.0, "type_effectiveness": 1.0}
                    ]
                spirit_move = random.choice(spirit_moves)
                
                result = execute_turn(battle_id, corrupted_spirit, chosen_monster, spirit_move, session)
                show_move_result(
                    f"Corrupted {corrupted_spirit.name} strikes back!", chosen_monster.nickname, spirit_move["name"], 
                    result["damage"], chosen_monster.current_stats["hp"]
                    )
                
                turn += 1

            # Remove temp attribute
            if hasattr(corrupted_spirit, "current_stats"):
                del corrupted_spirit.current_stats

            # Decide winner
            if corrupted_hp <= 0:
                xp, money = calculate_battle_rewards(player.id, battle_difficulty=1, session=session)
                typer.echo(f"\nCleansing complete! You earned {xp} XP and {money} coins.")
            else:
                typer.echo("\nYou lost the cleansing battle. Heal your monster and try again!")

    except Exception as e:
        typer.echo(f"Error during cleansing: {e}")
