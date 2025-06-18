import typer
from lib.db.connection import Session

app = typer.Typer()
session = Session()

@app.command()
def cleanse():
    """
    Cleanse a corrupted spirit (AI battle).
    """
    typer.echo("🔮 Starting cleansing battle...")
    # call your old cleanse logic here
    from .cleanse_cli import start

@app.command()
def pvp():
    """
    Challenge another player to a battle.
    """
    typer.echo("⚔️  Starting PVP battle...")
    # call your PVP flow here
    
