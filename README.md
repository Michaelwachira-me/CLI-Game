# Echoes of Gaia: Unite Elements, Restore the World

***

## Game Description 

The World and the people of `Gaia` once lived in unity. This world's key Spirits - elements of air, water, fire, and earch - maintained balance between human beings and nature. However, division, greed, and immorality corrupted Gaia's harmony and the Spirit's willingness to maintain balance. Currently, the Spirits hide in plain sight as corrupted and confused beings.

As a player, you are a `Seeker`, divinely selected to connect with the Spirits and restore Gaia's balance. 

In this game that draws from social realism, how well can you understand the monsters' pain, build trust, and enable healing that will restore humanity and nature?

Rather than trying to conquer the Monster, can you make the difficult decisions and build your spiritual strength to ensure that the Monsters emphathize with Gaia's call for balance? 

***

## Database Schema

`Echoes of Gaia` is a CLI-based game, drawing from the principles of SQLAlchemy's ORM. Therefore, to understand how one model(for instance, the Player) relates to the monsters' model (for instance, Monster_species), observe the attached Entity Relationship Diagram (ERD) https://dbdiagram.io/d/GAME-6848fa9e4aa7226ff856c218 

***

## GAME DEMO
Before engaging with the game on a development-basis, follow the video attached to understand the social embodiment and playing mechanics: https://www.loom.com/share/60c4bbf46e354c469acf85c35e0a2f61?sid=49026ab5-473e-41bc-b4a8-67c505774eb2 


## Features

- Explore Gaia’s mystical regions  
- Cleanse corrupted elemental spirits through turn-based battles  
- Bond and grow your spirit team  
- Trade spirits with other seekers  
- Check seeker status and manage resources  
- Save your journey in a database

## Tech Stack

- **Python 3.11**
- **SQLAlchemy** (ORM)
- **SQLite** (default database)
- **Typer** (beautiful CLI)
- **Alembic** (database migrations)

***

## Usage

To get started:
### Fork and clone this repository:

```console
$ git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>/lib
```

### Install dependencies and activate virtual environment:
Inside your directory, run `pipenv install && pipenv shell`.


### Reset and seed the database:

```console
$ cd lib/
$ python3 db/reset-db.py
```

This will:
- Delete the old SQLite database (gaia.db)

- Run all Alembic migrations

- Seed new fake data using Faker

### Using the CLI Tool:

Get started by running the CLI interface:

```console
$ python3 -m lib.cli.main run
```

You will be exposed to the main menu that aims at:
- Explore Gaia: Discover new elemental spirits.
- Cleanse Corruption: Battle corrupted spirits to purify them.
- Bond: Strengthen relationships with your spirits.
- Trade: Exchange spirits with other players (planned feature).
- Check Status: View coins, experience, and spirit details.

```console
=== Gaia Restoration ===
1. Explore Gaia
2. Cleanse Corruption (Battle)
3. Bond with Spirits
4. Propose a Trade
5. Check Seeker Status
6. Exit
```

`Follow Prompts to Play!`

###  Development and testing

To further explore and explore the relationship between the models and associated cli/ files, you can:

#### Using Typer Commands 

Each CLI component (e.g., explore, cleanse, trade ..) is implemented with typer.Typer(). You can run individual commands directly:

for instance, in your terminal, in the root of your project, run the following: 

```console
$ python3 -m lib.cli.main cleanse start
==> You should see corrupted spirit(monster) and choice to choose your spirit to battle with 
```

To run other commands, open individual CLI components in `lib/cli/` to understand and interact with the app commands. 

***

## Contributing
Pull requests are welcome!
If you have ideas for new features, please open an issue first.

1. Fork this repository
2. Create a new branch (git checkout -b feature/new-feature)
3. Commit your changes (git commit -m 'Add new feature')
4. Push to your branch (git push origin feature/new-feature)
5. Open a Pull Request

***

## Authors 
1. Wanjiru Muchiri (https://github.com/shirocodes)
2. MichaelWachira (https://github.com/Michaelwachira-me)

## License
This project is licensed under the MIT License.

        **May Gaia guide you, Seeker!**









