import typer
from rich.table import Table
from rich.console import Console

console = Console()

# helper functions to improve UI when players are in Battle arena
# used in cleanse_cli.py and battle_cli.py for DRY and UI
def display_turn(player_name, player_hp, opponent_name, opponent_hp):
    """
    show current turn status as the battle continues
    """
    # use table with title
    console.rule("[bold cyan] ⚔️  BATTLE ARENA ⚔️")
    table = Table(show_header=True, header_style="bold magenta")

    table.add_column(" Player", justify="center", style="green", no_wrap=True)
    table.add_column(" Opponent", justify="center", style="red", no_wrap=True)

    table.add_row(player_name, opponent_name)
    table.add_row(f"HP: {player_hp}", f"HP: {opponent_hp}")

    console.print(table)


def your_move_prompt():
    """
    helper func to help in prompting the player's or opponent's move
    """
    typer.secho(" You have the choice to attack or defend:", fg=typer.colors.BRIGHT_BLUE, bold=True)
    typer.echo("1.  Attack")
    typer.echo("2.  Defend")
    typer.echo("3. Surrender (End Battle)")
    move = int(typer.prompt("Choose your move (1 or 2 or 3)").strip())
    return move

def show_move_result(attacker, defender, move_name, damage, defender_hp):
    """
    after a move and round is over, use this HELPER to:
        - show results of either the player or opponent
    """
    typer.secho(f"\n{attacker} used {move_name} and dealt {damage} damage!", fg=typer.colors.YELLOW, bold=True)
    typer.secho(f"{defender} has {defender_hp} HP left.\n", fg=typer.colors.MAGENTA)

def show_separator():
    """
    clear separator for each turn in the battle
    """
    typer.secho("-" * 40, fg=typer.colors.BRIGHT_BLACK)


