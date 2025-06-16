import typer
from lib.cli.explore_cli import start

def explore_menu():
    typer.secho("\n Entering Gaia's wilds...", fg=typer.colors.CYAN)
    start()
    typer.echo()
    typer.secho("Press Enter to return to Main Menu.", fg=typer.colors.BRIGHT_BLACK)
    input()