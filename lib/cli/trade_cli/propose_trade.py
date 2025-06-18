import typer
import time
from lib.utilities.trade_system.trade_dynamics import propose_trade
from lib.utilities.monster_system.catch_monster import get_player_collection
from lib.utilities.player_system.create_player import login_player
from lib.models import Player
from lib.db.connection import Session
from lib.utilities.clear_screen import clear_screen

session = Session()

def propose_trade_flow():
    """
    Initiates a spirit trade proposal between Seekers.
    """
    try:
        typer.secho("\n=== SPIRIT TRADE HALL ===", fg=typer.colors.CYAN, bold=True)
        typer.secho("\nTo barter spirits is not mere exchange — it is a covenant to guide Gaia’s lost spirits toward harmony.\n", fg=typer.colors.BRIGHT_BLACK)

        # login via login_player helper func
        typer.secho("=== LOGIN ===", fg=typer.colors.CYAN, bold=True)
        username = typer.prompt("Your Seeker name")
        password = typer.prompt("Your secret phrase", hide_input=True)

        player = login_player(username, password)
        clear_screen()

        typer.secho(f"\nWelcome back, {player.username}.", fg=typer.colors.GREEN, bold=True)
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

        offered = typer.prompt("Enter numbers of spirits to offer, separated by commas")
        offered_ids = [collection[int(i.strip()) - 1].id for i in offered.split(",")]
            
            #  Enter other player username
        other_username = typer.prompt("Enter the username of the Seeker you want to trade with")
        to_player = session.query(Player).filter_by(username=other_username).first()

        if not to_player:
            typer.secho(f"No Seeker found with username: {other_username}", fg=typer.colors.RED)
            return

            # Request monsters in return
        typer.secho(f"\n {other_username}'s spirits:", fg=typer.colors.CYAN)
        other_collection = get_player_collection(to_player.id)
            
        for idx, mon in enumerate(other_collection, start=1):
            typer.echo(f"{idx}. {mon.nickname} (Lv.{mon.level}) Trust: {mon.experience}")
        requested = typer.prompt("Enter numbers of spirits you want in exchange (comma-separated)")
        requested_ids = [other_collection[int(i.strip()) - 1].id for i in requested.split(",")]
            
            # Propose trade using helper
        propose_trade(
            from_player=player.id,
            to_player=to_player.id,
            offered_monsters=offered_ids,
            requested_monsters=requested_ids
        )

        typer.secho("\n Trade proposal sent successfully! This exchange guide Gaia's harmony back into balance.", fg=typer.colors.GREEN)
 
    except Exception as e:
        typer.secho(f"  Error proposing trade: {e}", fg=typer.colors.RED)