import typer
from lib.utilities.monster_system.catch_monster import get_player_collection
from lib.db.connection import Session
from lib.models import Player

session= Session()
app = typer.Typer()

@app.command()
def show():
    """
    Display your Seeker status, team, and progress.
    """
    try:
        player_id = 1
        player = session.query(Player).get(player_id)

        typer.secho(f"\n Seeker: {player.username}", fg=typer.colors.CYAN)
        typer.echo(f"Level: {player.level}")
        typer.echo(f"money: {player.money}")
        typer.echo(f"XP: {player.experience}")

        typer.secho("\n Spirit Team:", fg=typer.colors.GREEN)
        collection = get_player_collection(player_id)
        
        if collection:
            for mon in collection:
                typer.echo(f"- {mon.nickname} (Lv.{mon.level}) Trust: {mon.experience}")
        else:
            typer.secho("You have no bonded spirits yet. Explore Gaia more.")
            
    except Exception as e:
        typer.secho(f"  Error fetching status: {e}", fg=typer.colors.RED)