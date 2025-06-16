import typer
from lib.cli.status_cli import show

def status_menu():
    typer.secho("\n Checking your Seeker status...", fg=typer.colors.CYAN)
    show()
    typer.echo()
    typer.secho("Press Enter to continue...", fg=typer.colors.BRIGHT_BLACK)
    input()