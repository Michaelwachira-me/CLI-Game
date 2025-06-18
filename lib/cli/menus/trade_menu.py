import typer
from lib.cli.trade_cli.propose_trade import propose_trade_flow
from lib.cli.trade_cli.view_trade import view_trades_flow
from lib.utilities.clear_screen import clear_screen

def trade_menu():
    while True:
        clear_screen()
        typer.secho("\n=== SPIRIT TRADE HALL ===", fg=typer.colors.CYAN, bold=True)
        typer.echo("1. Propose a Spirit Trade")
        typer.echo("2. View Your Trade Agreements")
        typer.echo("3. Return to Main Menu")

        choice = typer.prompt("Enter option (1-3)").strip()

        if choice == '1':
            try:
                propose_trade_flow()
            except Exception as e:
                typer.secho(f"Error proposing trade: {e}", fg=typer.colors.RED)

        elif choice == '2':
            try:
                view_trades_flow()
            except Exception as e:
                typer.secho(f"Error viewing trades: {e}", fg=typer.colors.RED)

        elif choice == '3':
            typer.secho("\nReturning to Main Menu...", fg=typer.colors.BRIGHT_BLUE)
            break

        else:
            typer.secho("\nInvalid input. Please choose 1, 2, or 3.", fg=typer.colors.RED)

        typer.echo()
        typer.secho("Press Enter to continue...", fg=typer.colors.BRIGHT_BLACK)
        input()
