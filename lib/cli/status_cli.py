import typer
from contextlib import contextmanager
from lib.utilities.monster_system.catch_monster import get_player_collection
from lib.utilities.player_system.create_player import login_player
from lib.models import Player, Player_achievement, Achievement
from lib.db.connection import Session
from lib.utilities.clear_screen import clear_screen

app = typer.Typer()

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
@app.command()
def show():
    """
    Display your Seeker status, spirit team, and achievements.
    """
    try:
        with get_session() as session:
            # Login for ANY player
            typer.secho("\n=== LOGIN ===", fg=typer.colors.CYAN, bold=True)
            username = typer.prompt("Your username")
            password = typer.prompt("Your password", hide_input=True)

            player = login_player(username, password)
            clear_screen()

            typer.secho(f"\nSeeker: {player.username}", fg=typer.colors.BRIGHT_CYAN)
            typer.echo(f"Level: {player.level}")
            typer.echo(f"XP: {player.experience}")
            typer.echo(f"Money: {player.money}")

            # Spirits
            typer.secho("\nBonded Spirits:", fg=typer.colors.GREEN)
            collection = get_player_collection(player.id)
            if collection:
                for mon in collection:
                    typer.echo(f"- {mon.nickname} (Lv.{mon.level}) Trust: {mon.experience}")
            else:
                typer.secho("You have no bonded spirits yet. Venture deeper into Gaia!")

            # Achievements
            typer.secho("\nAchievements:", fg=typer.colors.MAGENTA)
            player_achievements = session.query(Player_achievement).filter_by(player_id=player.id).all()

            if player_achievements:
                for pa in player_achievements: 
                    # Look up achievement name + description
                    achievement = session.query(Achievement).get(pa.achievement_id)
                    typer.echo(f"- {achievement.name}: {achievement.description} (Progress: {pa.progress}%)")
            else:
                typer.secho("You have no achievements yet. Keep exploring, battling and bonding!", fg=typer.colors.BRIGHT_BLACK)

    except Exception as e:
        typer.secho(f"Error fetching status: {e}", fg=typer.colors.RED)
