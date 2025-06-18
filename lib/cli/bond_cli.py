import typer
import time
from lib.db.connection import Session
from lib.utilities.monster_system.catch_monster import get_player_collection
from lib.utilities.monster_system.leveling_system import level_up_monster
from lib.utilities.player_system.create_player import login_player
from lib.utilities.battle_system.battle_ui import show_separator

app = typer.Typer()
session = Session()

@app.command()
def start():
    """
    Spend time bonding with one of your spirits to increase trust and strength.
    """
    try:
        # login via login_player helper func
        typer.secho("\n=== LOGIN ===", fg=typer.colors.CYAN, bold=True)
        username = typer.prompt("Your username")
        password = typer.prompt("Your password", hide_input=True)

        player = login_player(username, password)
        
        # enabling a clear transition for UI
        typer.clear()
        typer.secho(f"\nWelcome back, {player.username}!", fg=typer.colors.GREEN, bold=True)
        time.sleep(1)
        
        # Use correct player.id to get player's monster collection
        collection = get_player_collection(player.id)

        if not collection:
            typer.secho("You have no spirits yet. Explore Gaia first.", fg=typer.colors.RED)
            return

        # Let player pick
        typer.secho("\n Your current spirits:", fg=typer.colors.CYAN)
        for idx, mon in enumerate(collection, start=1):
            typer.echo(f"{idx}. {mon.nickname} (Lv.{mon.level}) Trust: {mon.experience}")

        choice_idx = int(typer.prompt("Choose a spirit to bond with")) - 1
        chosen_mon = collection[choice_idx]
        
        # another transition with time for emotional UI
        typer.clear()
        typer.secho(f"{chosen_mon.nickname} is yours.\n", fg=typer.colors.MAGENTA, bold=True)
        time.sleep(1)
        
            # display these msgs to reinforce Gaia Game's dynamics
        typer.echo("You sit quietly beside your spirit...")
        time.sleep(2)
        typer.echo("You feel its hidden pain, the corruption that turned it into a monster...")
        time.sleep(2)
        typer.echo("Your presence calms the chaos within.")
        time.sleep(2)
        typer.echo("This sacred bond helps purify its essence, slowly restoring Gaia's balance.")
        time.sleep(2)

        # Level up
        new_stats = level_up_monster(chosen_mon.id)
        typer.secho(f" {chosen_mon.nickname} feels your empathy and grows stronger.", fg=typer.colors.GREEN)
        
        show_separator() # input line separator for UI
        typer.secho("\n Your bond has unlocked a new level.", fg=typer.colors.GREEN, bold=True)
        typer.echo(f"New Level: {new_stats['level']}")
        typer.echo(f"Renewed Spirit Stats: {new_stats['current_stats']}")
        time.sleep(2)
        
        typer.secho("\nYour spiritual bond has mended a fragment of Gaia's broken harmony.", fg=typer.colors.BRIGHT_GREEN)
    except Exception as e:
        typer.secho(f" Error while bonding: {e}", fg=typer.colors.RED)