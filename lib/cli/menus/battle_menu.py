import typer
from lib.cli.battle_cli import cleanse, pvp

from cli.battle_cli import cleanse, pvp

def battle_menu():
    while True:
        print("\n=== Battle Menu ===")
        print("1. Cleanse Corruption (vs AI)")
        print("2. Challenge a Seeker (PVP)")
        print("3. Back to Main Menu")

        choice = input("Choose your battle mode: ")

        if choice == '1':
            cleanse()
        elif choice == '2':
            pvp()
        elif choice == '3':
            break
        else:
            print("Invalid choice, please try again.")
        
