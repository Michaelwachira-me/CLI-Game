import typer

from .explore_cli import app as explore_app
from .cleanse_cli import app as cleanse_app
from .bond_cli import app as bond_app
from .trade_cli import app as trade_app
from .status_cli import app as status_app

from .menus.explore_menu import explore_menu
from .menus.cleanse_menu import cleanse_menu
from .menus.bond_menu import bond_menu
from .menus.trade_menu import trade_menu
from .menus.status_menu import status_menu

from lib.utilities.clear_screen import clear_screen
app = typer.Typer()

# Add subcommands
app.add_typer(explore_app, name="explore", help="Venture into Gaia to calm lost spirits.")
app.add_typer(cleanse_app, name="cleanse", help="Cleanse corrupted spirits through battles.")
app.add_typer(bond_app, name="bond", help="Bond with your spirits to grow stronger.")
app.add_typer(trade_app, name="trade", help="Propose a trade.")
app.add_typer(status_app, name="status", help="View your Seeker's spirit collection and harmony status.")

@app.command()
def run():
    """
    Gaia Restoration - Main Menu
    """
    while True:
        clear_screen()
        typer.secho("\n=== Gaia Restoration ===", fg=typer.colors.CYAN, bold=True)
        typer.echo("1. Explore Gaia")
        typer.echo("2. Cleanse Corruption (Battle)")
        typer.echo("3. Bond with Spirits")
        typer.echo("4. Propose a Trade")
        typer.echo("5. Check Seeker Status")
        typer.echo("6. Exit")

        choice = typer.prompt("What will you do, Seeker?")

        if choice == '1':
            explore_menu()
        elif choice == '2':
            cleanse_menu()
        elif choice == '3':
            bond_menu()
        elif choice == '4':
            trade_menu()
        elif choice == '5':
            status_menu()
        elif choice == '6':
            typer.secho("Thank you, Seeker. May balance return to Gaia.", fg=typer.colors.MAGENTA)
            break
        else:
            typer.secho("Invalid choice. Try again, Seeker.", fg=typer.colors.RED)

if __name__ == "__main__":
    app()
