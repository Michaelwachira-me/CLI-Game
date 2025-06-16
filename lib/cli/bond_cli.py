import typer
from lib.models import Player
from lib.db.connection import Session
from lib.utilities.catch_monster import get_player_collection
from lib.utilities.leveling_system import level_up_monster

app = typer.Typer()
session = Session()

@app.command()
def start():
    """
    Spend time bonding with one of your spirits to increase trust and strength.
    """
    try:
        # login
        player_id = 1 
        player = session.query(Player).get(player_id)

        # Get your collection
        collection = get_player_collection(player_id)

        if not collection:
            typer.secho("You have no spirits yet. Explore Gaia first.", fg=typer.colors.RED)
            return

        # Let player pick
        typer.secho("\n Your current spirits:", fg=typer.colors.CYAN)
        for idx, mon in enumerate(collection, start=1):
            typer.echo(f"{idx}. {mon['nickname']} (Lv.{mon['level']}) Trust: {mon['expertise']}")

        choice_idx = int(typer.prompt("Choose a spirit to bond with")) - 1
        chosen_mon = collection[choice_idx]

        # Level up
        typer.secho(f"\n Spending time with {chosen_mon['nickname']}...", fg=typer.colors.MAGENTA)
        new_stats = level_up_monster(chosen_mon['id'])

        typer.secho(f" {chosen_mon['nickname']} feels closer to you.", fg=typer.colors.GREEN)
        typer.echo(f"New Level: {new_stats['level']}")
        typer.echo(f"Updated Stats: {new_stats['current_stats']}")

    except Exception as e:
        typer.secho(f" Error while bonding: {e}", fg=typer.colors.RED)