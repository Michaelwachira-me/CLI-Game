import typer
from lib.cli.cleanse_cli import start

def cleanse_menu():
    typer.secho("\n Preparing to cleanse corruption...", fg=typer.colors.CYAN)
    start()
    typer.echo()
    typer.secho("Press Enter to continue...", fg=typer.colors.BRIGHT_BLACK)
    input()