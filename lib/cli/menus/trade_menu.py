import typer
from lib.cli.trade_cli import start

def trade_menu():
    typer.secho("\nPreparing your trade proposal...", fg=typer.colors.CYAN)
    start()
    typer.echo()
    typer.secho("Press Enter to continue...", fg=typer.colors.BRIGHT_BLACK)
    input()