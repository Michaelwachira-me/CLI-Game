import typer
import time
from contextlib import contextmanager
from sqlalchemy.sql import func
from lib.models import Player, MonsterSpecies
from lib.utilities.monster_system.catch_rate import calculate_catch_rate
from lib.utilities.monster_system.catch_monster import catch_monster
from lib.utilities.player_system.create_player import login_player
from lib.db.connection import Session
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
    Venture into Gaia to calm a wandering spirit.
    """
    try:
        with get_session() as session:
            typer.echo("\n--- Gaia Wilds: A Whisper from the Beyond ---")
            time.sleep(1)
            
            # Login for player
            typer.secho("\n=== LOGIN ===", fg=typer.colors.CYAN, bold=True)
            username = typer.prompt("Your username")
            password = typer.prompt("Your password", hide_input=True)

            player = login_player(username, password, session)
            clear_screen()
            
            # game narrative to improve UI
            typer.secho(f"\nWelcome, {player.username}. Your inner harmony radiates at level {player.level}.", fg=typer.colors.BLUE) 
            time.sleep(1.5)
            
            typer.echo("\nA hush settles. Something stirs in the mist ahead...")
            time.sleep(2)
            
            # Introduce monster spirit for player to own
            spirit = session.query(MonsterSpecies).order_by(func.random()).first()
            typer.secho(f"\nBefore you drifts the spirit form of {spirit.name}.",fg=typer.colors.GREEN)
            typer.secho(
                f"Element: {spirit.element_type} | Essence: {spirit.rarity}", fg=typer.colors.BLACK, bold=True)
            time.sleep(1)
            
            typer.secho(
                "\nCalm this spirit and it may choose to stand beside you.\n"
                "Together, you may train and battle — restoring balance to Gaia and deepening your bond.",
                fg=typer.colors.YELLOW
            )
            time.sleep(1)
            
            choice = typer.prompt("\nDo you extend your aura and call to this spirit? (y/n)")
            if choice.lower() == 'y':
                typer.echo("\nYou breathe slowly, grounding your soul...")
                time.sleep(1.5)
                
                # evaluate chance of catching the monster spirit
                chance = calculate_catch_rate(spirit.rarity, player.level)
                typer.secho(
                    f"Your calming resonance reaches {round(chance * 100, 2)}% harmony.",
                    fg=typer.colors.BLUE
                )
                time.sleep(1)
                
                success = catch_monster(player.id, spirit.id, session)
                time.sleep(1)
                if success:
                    typer.secho(
                        f"\nA gentle warmth envelops you. The {spirit.name} spirit now trusts your care.",
                        fg=typer.colors.GREEN
                    )
                    typer.secho("\nVisit the training grounds or battle circles to strengthen this bond and guide Gaia toward balance.",
                                fg=typer.colors.BRIGHT_BLACK, bold=True)
                else:
                    typer.secho(
                        f"\nA fleeting whisper... The {spirit.name} spirit drifts back to the unseen veil.",
                        fg=typer.colors.YELLOW
                    )
                    typer.secho("\nVisit the battle arena to guide Gaia toward balance in a different way.",
                                fg=typer.colors.BRIGHT_BLACK, bold=True)
            else:
                typer.secho(
                    "\nYou bow your head. Some encounters are not meant to bind today.",
                    fg=typer.colors.BLUE
                )
                typer.secho("\nVisit the battle arena to guide Gaia toward balance in a different way.",
                                fg=typer.colors.BRIGHT_BLACK, bold=True)
    except Exception as e:
        typer.secho(f"Ooops! A rift in the flow: {e}", fg=typer.colors.RED)