import typer
from lib.models import Player, MonsterSpecies, PlayerMonster
from lib.utilities.battle_system.create_battle import create_battle
from lib.utilities.battle_system.combat_system import (
    execute_turn,
    check_battle_end,
    calculate_battle_rewards
)
from lib.db.connection import Session
from sqlalchemy.sql import func

app = typer.Typer()
session = Session()

@app.command()
def start():
    """
    Cleanse a corrupted Elemental Spirit through battle.
    """

    try:
        # Get player
        player_id = 1  # Hardcoded for now
        player = session.query(Player).get(player_id)

        # Pick random corrupted spirit
        corrupted_spirit = session.query(MonsterSpecies).order_by(func.random()).first()
        typer.secho(f"\nA corrupted spirit emerges: {corrupted_spirit.name} ({corrupted_spirit.element_type})!", fg=typer.colors.RED)

        # === 3. Show player's team ===
        player_team = player.monsters
        if not player_team:
            typer.secho("You have no spirits to battle with! Explore Gaia first.", fg=typer.colors.RED)
            return

        typer.secho("\nChoose your spirit to battle with:", fg=typer.colors.CYAN)
        for idx, mon in enumerate(player_team, start=1):
            typer.echo(f"{idx}. {mon.nickname} (Lv.{mon.level}) HP: {mon.current_stats['hp']}")

        chosen_idx = int(typer.prompt("Enter the number of your chosen spirit")) - 1
        chosen_monster = player_team[chosen_idx]

        # === 4. Create battle ===
        battle = create_battle(
            player1_id=player_id,
            player2_id=None,
            monster_teams=[[chosen_monster.id]]
        )
        battle_id = battle['battle_id']

        typer.secho("\nThe battle to cleanse begins!", fg=typer.colors.MAGENTA)

        # === 5. Battle loop ===
        turn = 1
        while not check_battle_end(battle_id):
            # Always fetch fresh monster by ID (safe!)
            attacker_monster_id = battle['monster_teams'][0][0]
            attacker_monster = session.query(PlayerMonster).get(attacker_monster_id)

            typer.secho(f"\nTurn {turn}:", fg=typer.colors.BRIGHT_BLUE)
            typer.echo(f"{attacker_monster.nickname} vs corrupted {corrupted_spirit.name}")

            typer.echo("1. Spirit Strike (Powerful)")
            typer.echo("2. Guard (Reduce damage)")
            move = int(typer.prompt("Choose your move"))

            # Do turn
            turn_result = execute_turn(
                battle_id=battle_id,
                attacker_monster=attacker_monster,
                defender_monster=corrupted_spirit,
                move=move
            )

            typer.secho(
                turn_result['message'],
                fg=typer.colors.GREEN if turn_result['success'] else typer.colors.RED
            )

            turn += 1

        # === 6. Check who won ===
        winner = turn_result['winner']
        if winner == player_id:
            reward, xp = calculate_battle_rewards(player_id, battle['difficulty'])
            typer.secho(
                f"\nCleansing complete! You gained {reward} coins and {xp} spirit experience.",
                fg=typer.colors.GREEN
            )
        else:
            typer.secho(
                "\nYou were overwhelmed. Restore your spirits and try again.",
                fg=typer.colors.RED
            )

    except Exception as e:
        typer.secho(f"\nError during cleansing: {e}", fg=typer.colors.RED)
