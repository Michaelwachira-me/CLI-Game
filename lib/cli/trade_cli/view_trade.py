import typer
from lib.models import Trade, PlayerMonster
from lib.db.connection import Session
from lib.utilities.player_system.create_player import login_player
from lib.utilities.clear_screen import clear_screen

session = Session()

def view_trades_flow():
    """
    Lets a Seeker view incoming trades and accept or decline them.
    """
    clear_screen()
    typer.secho("\n=== SPIRIT TRADE RECORDS ===", fg=typer.colors.CYAN, bold=True)

    typer.secho("\nIn Gaia's path, harmony demands fair exchanges. Review what other Seekers offer you.", fg=typer.colors.BRIGHT_BLACK)

    # login player
    typer.secho("\n=== LOGIN ===", fg=typer.colors.CYAN, bold=True)
    username = typer.prompt("Your Seeker name")
    password = typer.prompt("Your secret phrase", hide_input=True)

    player = login_player(username, password)
    clear_screen()

    typer.secho(f"\nWelcome, {player.username}.", fg=typer.colors.GREEN, bold=True)

    # GET incoming trades
    trades = session.query(Trade).filter_by(to_playerID=player.id, status="pending").all()

    if not trades:
        typer.secho("\nNo trade proposals await you at this moment.", fg=typer.colors.BRIGHT_BLACK)
        return

    # List existing trades
    for idx, trade in enumerate(trades, start=1):
        typer.secho(f"\nTrade #{idx}: (Trade ID: {trade.id})", fg=typer.colors.CYAN, bold=True)

        # when proposing trades, player listed them with "," so use .join
        offered = ', '.join(
            [session.query(PlayerMonster).get(mid).nickname for mid in trade.offered_monsters]
        )
        requested = ', '.join(
            [session.query(PlayerMonster).get(mid).nickname for mid in trade.requested_monsters]
        )

        typer.echo(f"Monster spirit {offered} offered to you")
        typer.echo(f"In exchange, you will offer: Monster spirit {requested}")
        typer.echo(f"Status: {trade.status}")

    # Choose trade to accept or decline
    trade_id = typer.prompt("\nEnter the Trade ID you wish to process")
    choice = typer.prompt("Accept this trade? (yes/no)").lower()

    from lib.utilities.trade_system.trade_dynamics import accept_or_decline_trade

    if choice in ["yes", "y"]:
        result = accept_or_decline_trade(int(trade_id), accept=True)
    else:
        result = accept_or_decline_trade(int(trade_id), accept=False)

    typer.secho(f"\n{result}", fg=typer.colors.GREEN if 'accepted' in result else typer.colors.RED)
