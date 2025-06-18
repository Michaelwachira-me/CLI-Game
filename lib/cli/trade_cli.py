import typer
from lib.utilities.trade_system.trade_dynamics import propose_trade
from lib.utilities.monster_system.catch_monster import get_player_collection
from lib.models import Player
from lib.db.connection import Session

app = typer.Typer()
session = Session()

@app.command()
def start():
    """
    Propose a trade with another Seeker.
    """
    try:
        # login
        from_player_id = 1
        from_player = session.query(Player).get(from_player_id)

        # Pick your monsters to offer
        collection = get_player_collection(from_player_id)
        if not collection:
            typer.secho("You have no spirits to trade yet.", fg=typer.colors.RED)
            return

        typer.secho("\n Your available spirits:", fg=typer.colors.CYAN)
        for idx, mon in enumerate(collection, start=1):
            typer.echo(f"{idx}. {mon['nickname']} (Lv.{mon['level']})")

        offered = typer.prompt("Enter numbers of spirits to offer, separated by commas")
        offered_ids = [collection[int(i.strip()) - 1]['id'] for i in offered.split(",")]

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
            typer.echo(f"{idx}. {mon['nickname']} (Lv.{mon['level']})")

        requested = typer.prompt("Enter numbers of spirits you want in exchange (comma-separated)")
        requested_ids = [other_collection[int(i.strip()) - 1]['id'] for i in requested.split(",")]

        # Propose trade using helper
        propose_trade(
            from_player=from_player,
            to_player=to_player,
            offered_monsters=offered_ids,
            requested_monsters=requested_ids
        )

        typer.secho("\n Trade proposal sent successfully!", fg=typer.colors.GREEN)

    except Exception as e:
        typer.secho(f"  Error proposing trade: {e}", fg=typer.colors.RED)