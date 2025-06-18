import typer
import random
from lib.db.connection import Session
from .cleanse_cli import start as cleanse_battle
from lib.models import Player
from lib.utilities.battle_system.create_battle import create_battle
from lib.utilities.battle_system.combat_system import execute_turn, calculate_battle_rewards
from lib.utilities.player_system.create_player import create_player, login_player

app = typer.Typer()
session = Session()

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
        typer.secho("\n=== LOGIN ===", fg=typer.colors.CYAN, bold=True)
        username = typer.prompt("Your username")
        password = typer.prompt("Your password", hide_input=True)
        player = login_player(username, password)
        typer.secho(f"\n Welcome back, {player.username}!", fg=typer.colors.GREEN, bold=True)

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
        
        typer.secho("\n=== YOUR MONSTERS ===", fg=typer.colors.CYAN, bold=True)
        for idx, m in enumerate(player.monsters, 1):
            typer.echo(f"{idx}. {m.nickname} (Lv.{m.level})")

        chosen_index = int(typer.prompt("Pick your monster number")) - 1
        chosen_monster = player.monsters[chosen_index]
        chosen_monster.initialize_current_stats()
        
        # Opponent's strongest
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
        )
        battle_id = battle["battle_id"]

        typer.secho("\n BATTLE STARTS! ", fg=typer.colors.GREEN, bold=True)

        turn = 1
        while chosen_monster.current_stats["hp"] > 0 and opponent_monster.current_stats["hp"] > 0:
            typer.secho("\n" + "="*30, fg=typer.colors.BLUE)
            typer.secho(f" TURN {turn}", fg=typer.colors.BLUE, bold=True)
            typer.echo(f" Your {chosen_monster.nickname} HP: {chosen_monster.current_stats['hp']}")
            typer.echo(f" {opponent.username}'s {opponent_monster.nickname} HP: {opponent_monster.current_stats['hp']}")

            typer.echo("\n Your Move:")
            typer.echo("1.  Attack")
            typer.echo("2.  Defend")
            move_choice = int(typer.prompt("Choose move (1 or 2)"))

            player_move = {
                "name": "Attack", "power": 1.5, "type_effectiveness": 1.0
            } if move_choice == 1 else {
                "name": "Defend", "power": 0.5, "type_effectiveness": 1.0
            }

            result = execute_turn(battle_id, chosen_monster, opponent_monster, player_move)
            typer.echo(result["log"])

            if opponent_monster.current_stats["hp"] <= 0:
                break

            # Opponent AI move
            typer.echo(f"\n {opponent.username}'s Move:")
            opponent_move = random.choice([
                {"name": "Attack", "power": 1.5, "type_effectiveness": 1.0},
                {"name": "Defend", "power": 0.5, "type_effectiveness": 1.0}
            ])
            result = execute_turn(battle_id, opponent_monster, chosen_monster, opponent_move)
            typer.echo(result["log"])

            turn += 1

        # Winner plus rewarding
        if chosen_monster.current_stats["hp"] > 0:
            xp, money = calculate_battle_rewards(player.id, battle_difficulty=2)
            typer.secho(f"\n YOU WIN! {opponent.username} is defeated!", fg=typer.colors.GREEN, bold=True)
            typer.secho(f" Rewards: +{xp} XP, +{money} coins!", fg=typer.colors.YELLOW, bold=True)
        else:
            xp, money = calculate_battle_rewards(opponent.id, battle_difficulty=2)
            typer.secho(f"\n YOU LOSE! {opponent.username} wins this round!", fg=typer.colors.RED, bold=True)
            typer.secho(f" {opponent.username} earns +{xp} XP, +{money} coins.", fg=typer.colors.YELLOW, bold=True)

        typer.secho("\n Thanks for battling — train and fight again soon!", fg=typer.colors.MAGENTA, bold=True)

    except Exception as e:
        typer.secho(f"\n ERROR: {e}", fg=typer.colors.RED, bold=True)
