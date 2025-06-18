import typer
from lib.cli.battle_cli import cleanse, pvp
from lib.utilities.clear_screen import clear_screen

def battle_menu():
    while True:
        clear_screen()
        typer.secho("\n=== BATTLE MENU ===", fg=typer.colors.CYAN, bold=True)
        typer.echo("1. Cleanse Corruption (vs AI)")
        typer.echo("2. Challenge a Seeker (PVP)")
        typer.echo("3. Back to Main Menu")

        choice = typer.prompt("Enter option (1-3)").strip()

        if choice == '1':
            try:
                cleanse()
            except Exception as e:
                typer.secho(f"Error starting cleansing: {e}", fg=typer.colors.RED)

        elif choice == '2':
            try:
                pvp()
            except Exception as e:
                typer.secho(f"Error starting PVP battle: {e}", fg=typer.colors.RED)

        elif choice == '3':
            typer.secho("\nReturning to Main Menu...", fg=typer.colors.BRIGHT_BLUE)
            break

        else:
            typer.secho("\n Invalid input. Please choose 1, 2, or 3.", fg=typer.colors.RED)

        typer.echo()
        typer.secho("Press Enter to continue...", fg=typer.colors.BRIGHT_BLACK)
        input()
