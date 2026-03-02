from time import sleep as wait
import os, json

# import rich
try:
    from rich.console import Console
    from rich.traceback import install
except ModuleNotFoundError:
    input("Please Install rich first.")
    exit()

install(); del install
console = Console()

# Config
DELAY_TIME = 1

# Custom Error
class VersionError(Exception):
    pass
class CorrectVersionError(Exception):
    pass

def load(goal="continue"):
    with console.status(f"[blink dim]Press enter to {goal}", spinner="clock"):
        console.input()

# Checking
try:
    with console.status("Checking Data..."):
        data_path = os.path.dirname(os.path.abspath(__file__))
        all_data_path = os.path.join(data_path, "All Data.json")

        # Load Data -> data
        with open(all_data_path, "r") as file:
            data = json.load(file)

        # Checking Version
        if data["Version"] == [1, 12,0, None]: raise CorrectVersionError# If upgraded
        elif data["Version"][0] != 1 or data["Version"][1] != 11: raise VersionError # If not the correct version
        wait(DELAY_TIME)
except FileNotFoundError:
    console.print("[bold red]ERROR:[/] Please move this file to calculator's data directory")
    load("quit")
    quit()
except VersionError:
    console.print("[bold red]ERROR:[/] Please upgrade from v1.11.4 to v1.12.0")
    load("quit")
    quit()
except CorrectVersionError:
    console.print("[bold green]ERROR:[/] Your data has been upgraded to v1.12.0+")
    load("quit")
    quit()

# Asking
Input = console.input("Your data is ready to upgrade, whould you like to do it? [Y/n]    ").lower()
if Input == "n":
    load("quit")
    quit()

# Change
with console.status("Upgrading Data...", spinner="arc"):
    data["Version"] = [1, 12, 0, None]
    wait(DELAY_TIME)

# Write
try:
    with console.status("Replacing Data...", spinner="arc"):
        if not os.path.exists(all_data_path): raise FileNotFoundError
        with open(all_data_path, "w") as file:
            json.dump(data,  file, indent=4)
        wait(DELAY_TIME)
except FileNotFoundError:
    console.print("[bold red]ERROR:[/] Can't find data file.")
    load("quit")
    quit()

# Complete
console.print("    [bold green]Update data file successfully!")
console.print("    [dim]Please replace your calculator.py with the new version before using the calculator.")
load("quit")