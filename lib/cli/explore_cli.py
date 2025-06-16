import typer
from sqlalchemy.sql import func
from lib.models import Player, MonsterSpecies
from lib.utilities.catch_rate import calculate_catch_rate
from lib.utilities.catch_monster import catch_monster
from lib.db.connection import Session

app = typer.Typer()
session = Session()

@app.command()
def start():
    """
    Venture into Gaia to calm a wandering spirit.
    """
    try:
        spirit = session.query(MonsterSpecies).order_by(func.random()).first()
        typer.secho(
            f"\n You sense a wandering spirit: {spirit.name} ({spirit.element_type})",
            fg=typer.colors.GREEN
        )
        choice = typer.prompt("Approach this spirit? (y/n)")
        if choice.lower() == 'y':
            player_id = 1 
            player = session.query(Player).get(player_id)
            chance = calculate_catch_rate(spirit.rarity, player.level)

            typer.secho(f"Your calming aura: {round(chance * 100, 2)}%", fg=typer.colors.BLUE)
            success = catch_monster(player_id, spirit.id)
            if success:
                typer.secho(f"The {spirit.name} spirit trusts you now.", fg=typer.colors.GREEN)
            else:
                typer.secho(f"The {spirit.name} spirit slips back into the mist...", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"  Error during exploration: {e}", fg=typer.colors.RED)