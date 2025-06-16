import typer
from lib.cli.bond_cli import start

def bond_menu():
    typer.secho("\n Entering a bonding session with your spirit...", fg=typer.colors.CYAN)
    start()
    typer.echo()
    typer.secho("Press Enter to continue...", fg=typer.colors.BRIGHT_BLACK)
    input()