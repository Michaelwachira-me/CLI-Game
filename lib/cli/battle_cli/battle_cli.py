import typer
import random
from contextlib import contextmanager
from lib.db.connection import Session
from .cleanse_cli import start as cleanse_battle
from lib.models import Player
from lib.utilities.battle_system.create_battle import create_battle
from lib.utilities.battle_system.combat_system import execute_turn, calculate_battle_rewards
from lib.utilities.player_system.create_player import login_player
from lib.utilities.battle_system.battle_ui import (
    show_separator, 
    display_turn, 
    your_move_prompt, 
    show_move_result
)
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
def cleanse():
    """
    Cleanse a corrupted spirit (AI battle).
    reusing cleanse_cli' logic
    """
    cleanse_battle()
    

@app.command()
def pvp():
    """
    Challenge another player to a battle.
    """
    try:
        with get_session() as session:
            # authenticate player 
            typer.secho("\n=== LOGIN ===", fg=typer.colors.CYAN, bold=True)
            username = typer.prompt("Your username")
            password = typer.prompt("Your password", hide_input=True)
            player = login_player(username, password, session)
            typer.secho(f"\n Welcome back, {player.username}!", fg=typer.colors.GREEN, bold=True)

            # Find player's opponent
            typer.secho("\n=== CHALLENGE AN OPPONENT ===", fg=typer.colors.CYAN, bold=True)
            opponent_username = typer.prompt("Enter opponent's username")

            opponent = session.query(type(player)).filter_by(username=opponent_username).first()
            if not opponent:
                typer.secho(f"\n Opponent '{opponent_username}' not found!", fg=typer.colors.RED, bold=True)
                return

            typer.secho(
                f"\n TRAINER {opponent.username.upper()} ACCEPTS YOUR CHALLENGE! ",
                fg=typer.colors.MAGENTA,
                bold=True,
            )
            
            # Both player pick their monster spirits
            typer.secho("\n=== YOUR MONSTERS ===", fg=typer.colors.CYAN, bold=True)
            for idx, m in enumerate(player.monsters, 1):
                typer.echo(f"{idx}. {m.nickname} (Lv.{m.level})")

            chosen_index = int(typer.prompt("Pick your monster number")) - 1
            chosen_monster = player.monsters[chosen_index]
            chosen_monster.initialize_current_stats()
            
            # system picks the Opponent's best monster
            opponent_monster = max(opponent.monsters, key=lambda m: m.level)
            opponent_monster.initialize_current_stats()
            typer.secho(
                f"\n {opponent.username}'s champion, {opponent_monster.nickname} (Lv.{opponent_monster.level}), enters the arena!",
                fg=typer.colors.YELLOW,
                bold=True,
            )
            
            # Create battle
            battle = create_battle(
                player1_id=player.id,
                player2_id=opponent.id,
                monster_teams={
                    "player1": [chosen_monster.id],
                    "player2": [opponent_monster.id],
                },
                session=session
            )
            battle_id = battle["battle_id"]

            typer.secho("\n BATTLE STARTS! ", fg=typer.colors.GREEN, bold=True)

            # Initialize battle loop=> players taking turns till one wins
            turn = 1
            while chosen_monster.current_stats["hp"] > 0 and opponent_monster.current_stats["hp"] > 0:
                show_separator()
                
                typer.secho(f" BATTLE ROUND {turn} ", fg=typer.colors.BLUE, bold=True)
                # display turns via helper func.
                display_turn(
                    chosen_monster.nickname,
                    chosen_monster.current_stats["hp"],
                    opponent_monster.nickname,
                    opponent_monster.current_stats["hp"]
                )

                # propmt player to make a move via helper func
                move_choice = your_move_prompt()
                    # Since move_choices are 3 -> Attack, Defend, Surrender
                        # Handle the case where the player surrenders:
                if move_choice == 3:
                    typer.secho("\n You chose to surrender!", fg=typer.colors.RED, bold=True)
                    xp, money = calculate_battle_rewards(opponent.id, battle_difficulty=2, session=session)
                    typer.secho(
                        f"{opponent.username} wins by forfeit! +{xp} XP, +{money} coins.",
                        fg=typer.colors.YELLOW, bold=True
                    )
                    typer.secho("Returning to Battle Menu...", fg=typer.colors.BRIGHT_BLUE)
                    return
                    
                # otherwise, if player chooses Attack or Defend, pick move:
                player_move = {
                    "name": "Attack", "power": 1.5, "type_effectiveness": 1.0
                } if move_choice == 1 else {
                    "name": "Defend", "power": 0.5, "type_effectiveness": 1.0
                }

                # Execute player1' turn and show results using battle_ui's helper func.
                result = execute_turn(battle_id, chosen_monster, opponent_monster, player_move, session)
                show_move_result(
                    chosen_monster.nickname,
                    opponent_monster.nickname,
                    player_move["name"],
                    result["damage"],
                    opponent_monster.current_stats["hp"]
                )
                # typer.echo(result["log"])
                
                # If opponent is defeated, break loop
                if opponent_monster.current_stats["hp"] <= 0:
                    break

                # Opponent AI move
                typer.secho(f" {opponent.username}'s turn:", fg=typer.colors.BRIGHT_RED, bold=True)
                opponent_move = random.choice([
                    {"name": "Attack", "power": 1.5, "type_effectiveness": 1.0},
                    {"name": "Defend", "power": 0.5, "type_effectiveness": 1.0}
                ])
                result = execute_turn(battle_id, opponent_monster, chosen_monster, opponent_move, session)
                # typer.echo(result["log"])
                show_move_result(
                    opponent_monster.nickname,
                    chosen_monster.nickname,
                    opponent_move["name"],
                    result["damage"],
                    chosen_monster.current_stats["hp"]
                )

                turn += 1 #continue rounds till a winner arises

            # anounce winner and reward
            show_separator()
            if chosen_monster.current_stats["hp"] > 0:
                xp, money = calculate_battle_rewards(player.id, battle_difficulty=2, session=session)
                typer.secho(f"\n YOU WIN! {opponent.username} is defeated!", fg=typer.colors.GREEN, bold=True)
                typer.secho(f" Rewards: +{xp} XP, +{money} coins!", fg=typer.colors.YELLOW, bold=True)
            else:
                xp, money = calculate_battle_rewards(opponent.id, battle_difficulty=2, session=session)
                typer.secho(f"\n YOU LOSE! {opponent.username} wins this round!", fg=typer.colors.RED, bold=True)
                typer.secho(f" {opponent.username} earns +{xp} XP, +{money} coins.", fg=typer.colors.YELLOW, bold=True)

            typer.secho("\n Thanks for battling — train and fight again soon!", fg=typer.colors.MAGENTA, bold=True)

    except Exception as e:
        typer.secho(f"\n ERROR: {e}", fg=typer.colors.RED, bold=True)
