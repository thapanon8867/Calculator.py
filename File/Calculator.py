# Calculator.py
VERSION = [1, 12, 0, None]

# Import things
import math
import time
import os
import json

# Import Rich
try:
    from rich.console import Console
    from rich.align import Align
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.table import Table
    from rich.spinner import Spinner
    from rich.traceback import install as tbinstall
except ModuleNotFoundError:
    input("Please Install rich first.")
    exit()

# Configs
VERSION_MESSAGE = f"Version {VERSION[0]}.{VERSION[1]}.{VERSION[2]}"
SLEEP_TIME = 1
CLOSE_TIME = 4
VALUEERROR = "[bold red]Invalid input!: Try again."
ZERODIVISIONERROR = "[bold red]Cann't divided by zero!"
OVERFLOWERROR = "[bold red]Result is too large!"
ERROR = "[bold red]An expected error occurred:"

tbinstall(); del tbinstall
console = Console()
layout = Layout()

# Custom Errors
class VersionError(Exception):
    pass

# Center Functions
def Ask2number(Aprompt="A? > ", Bprompt="B? > ") :
    # Ask
    while True :
        try :
            #Ask A
            a = float(console.input(f"[bold dim]{Aprompt}").replace(",", ""))
            #Ask B
            b = float(console.input(f"[bold dim]{Bprompt}").replace(",", ""))
            break
        except ValueError :
            console.print(VALUEERROR, "\n")
    return a, b

def Ask1number(Aprompt="A? > ") :
    # Ask
    while True :
        try :
            #Ask A
            a = float(console.input(f"[bold dim]{Aprompt}").replace(",", ""))
            break
        except ValueError :
            console.print(VALUEERROR, "\n")
    return a

def processOperation(op_func, symbol, Aprompt="A? > ", Bprompt="B? > "):
    try:
        a, b = Ask2number(Aprompt, Bprompt)
        with console.status("[bold green]Thinking..."):
            # Finding Answer
            answer = op_func(a,b)
            if answer == int(answer): answer = int(answer) # If can int then int

            # Saving
            if Data["SaveHistories"]:
                Data["Histories"].append(f"{a} {symbol} {b} = {answer}")
            
            time.sleep(SLEEP_TIME)
        console.print(f"[bold yellow]Answer = {answer}")
    except OverflowError:
        console.print(OVERFLOWERROR)
    except Exception as e:
        console.print(ERROR, e)

# Operator Functions
def Plus() :
    processOperation(lambda a, b: a + b, "+")

def Minus() :
    processOperation(lambda a, b: a - b, "-")

def Times() :
    processOperation(lambda a, b: a * b, "*")

def Divide() :
    try :
        a, b = Ask2number()
        with console.status("[bold green]Thinking..."):
            # Finding Answer
            answer = a / b
            if answer == int(answer): answer = int(answer) # If can int then int
            remainder = a % b

            # Saving
            if Data["SaveHistories"]:
                Data["Histories"].append(f"{a} / {b} = {answer}")
            
            time.sleep(SLEEP_TIME)
        console.print(f"[bold yellow]Answer = {answer}")
        console.print(f"[dim yellow]Remainder = {remainder}")
    except ZeroDivisionError :
        console.print(ZERODIVISIONERROR)
    except OverflowError:
        console.print(OVERFLOWERROR)
    except Exception as e :
        console.print(ERROR , e)

def Power() :
    processOperation(lambda a, b: a ** b, "**", Bprompt="Power of ")

def Root() :
    try :
        console.print("[bold green]nth root of a number")
        n, a = Ask2number("n? > ", "a? > ")
        with console.status("[bold green]Thinking..."):
            if a <= 0 and n % 2 != 0: raise ValueError # base can't be below zero or zero when the index is a even number
            if n <= 0: raise ValueError # index can't be below zero or zero

            # Finding Answer
            answer = a ** (1/n)
            if answer == int(answer): answer = int(answer)

            # Saving
            if Data["SaveHistories"]:
                Data["Histories"].append(f"{a} ^ (1/{n}) = {answer}")
            
            time.sleep(SLEEP_TIME)
        console.print(f"[bold yellow]Answer = {answer}")
    except ValueError :
        console.print(VALUEERROR)
    except OverflowError:
        console.print(OVERFLOWERROR)
    except Exception as Reason :
        console.print(ERROR , Reason)

def Factorial() :
    try:
        a = int(Ask1number())
        with console.status("[bold green]Thinking..."):
            if a > 1000: raise OverflowError

            # Finding Answer
            answer = math.factorial(a)

            # Saving
            if Data["SaveHistories"]:
                Data["Histories"].append(f"{a}! = {answer}")
            
            time.sleep(SLEEP_TIME)
        console.print(f"[bold yellow]Answer = {answer}")
    except ValueError :
        console.print(VALUEERROR)
    except OverflowError:
        console.print(OVERFLOWERROR)
    except Exception as e :
        console.print(ERROR , e)

# Save Class
class DataHandler :
    # Locate data center
    script = os.path.abspath(__file__)
    script_parent = os.path.dirname(script)
    data_center = os.path.join(script_parent, "Data")
      
    def __init__(self, file_name:str, dataTemplate) :
        # Define File Name
        self.__name = file_name
        self.__path = os.path.join(self.data_center, self.__name) # dataCenter + filename = path

        DataHandler.__checkDataCenter()
        
        # Check File
        if os.path.exists(self.__path) : # If this path exists:
            self.__everExists = True
        else :
            self.__everExists = False

        if not self.__everExists: self.save(dataTemplate); data = dataTemplate # If file has not ever existed, push dataTemplate
    
    @staticmethod
    def __checkDataCenter(autoMk=True):
        data_center = DataHandler.data_center
        if not os.path.exists(DataHandler.data_center): # If data center doesn't exist:
            if autoMk: os.mkdir(data_center) # Create
            return False
        else:
            return True
        
    def save(self, data) :
        try :
            DataHandler.__checkDataCenter()
            with open(self.__path, "w") as file :
                json.dump(data, file, indent=4) # Push
        except FileNotFoundError as e:
            console.print(f"[bold red]Error while saving data: File Not Found [/]-- {e}")
        except Exception as e :
            console.print("[bold red]Error while saving data:", e)
    
    @property
    def data(self) :
        try :
            with open(self.__path,"r") as file :
                data = json.load(file) # Pull
            
            if data["Version"] != VERSION: # Check Version
                raise VersionError

            return data # Send
        except VersionError:
            console.print(f"[bold red]Wrong Version:[/] Please make sure that the data has exactly the same version as the calculator.")
        except FileNotFoundError as e:
            console.print(f"[bold red]Error while geting data:[/] File Not Found -- {e} -- Then restart the program.")
        except Exception as e :
            console.print("[bold red]Error while geting data:", e)

# Functions
def WhatsNew() :
    message = Table(box=None, show_header=False)
    message.add_row("1.", "Fix any unclear operation descriptions.")
    message.add_row("2.", "Use Library Rich to make the terminal colorful and easy to read.")

    panel = Panel(
        message,
        title=f"[bold]What's new?[/] [dim italic]-- v{VERSION[0]}.{VERSION[1]}.{VERSION[2]}-{VERSION[3] or "0"}",
        expand=False
    )
    console.print(panel)

def Move() :
    console.clear()

def ShowHistories(data) :
    histories = data["Histories"]

    # Create Table
    hisTable = Table(box=None, header_style="bold")
    hisTable.add_column("No.",justify="left",)
    hisTable.add_column("Operation",justify="right")

    if len(histories) == 0 : # if has no history
        hisTable.add_row(Align.center("[bold yellow]~~ No history ~~"))
    else :
        for i, item in enumerate(histories, 1) :
            hisTable.add_row(f"{str(i)}.", item)

    # Panel
    hisPanel = Panel(hisTable, title="[bold]Calculation Histories", expand=False)
    console.print(hisPanel) # print Panel
    if data["SaveHistories"]: console.print(f"[bold][cyan]Save History? = [/cyan][green]{data["SaveHistories"]}")
    else: console.print(f"[bold][cyan]Save History? = [/cyan][red]{data["SaveHistories"]}")

    # Del?
    Input = console.input("[bold]Do you want to clear histories? \\[y/N]    ").lower()
    if Input == "y":
        with console.status("[bold green]Working...") as _: # Make Loading
            data["Histories"] = []
            time.sleep(SLEEP_TIME)
        console.print("    [bold yellow]Histories cleared.")
    
    # Toggle?
    Input = console.input("[bold]Toggle histories? \\[y/N]    ").lower()
    if Input == "y":
        with console.status("[bold green]Working...") as _:
            data["SaveHistories"] = not data["SaveHistories"]
            time.sleep(SLEEP_TIME)
        code = "green" if data["SaveHistories"] else "red"
        ncode = "red" if data["SaveHistories"] else "green"
        console.print(f"    [bold][yellow]Toggled from [/yellow][{ncode}]{not data["SaveHistories"]}[/{ncode}] -> [{code}]{data["SaveHistories"]}[/{code}].")

    return data

def getMenuPanel():
    # Create Menu Table
    menu_table = Table(box=None, show_header=False)
    menu_table.add_row("1.", "Plus")
    menu_table.add_row("2.", "Minus")
    menu_table.add_row("3.", "Times")
    menu_table.add_row("4.", "Divide")
    menu_table.add_row("5.", "Power")
    menu_table.add_row("6.", "Root")
    menu_table.add_row("7.", "!")
    menu_table.add_row("h.", "Histories")
    menu_table.add_row("n.", "What's new?")
    menu_table.add_row("l.", "Leave")

    # Return Panel
    menu = Panel(menu_table, title="Menu", expand=False)
    return menu

def Run(data) :
    Move()
    console.print(f"[bold underline white]{VERSION_MESSAGE}")

    while True :
        console.print(getMenuPanel())
        Input = console.input("[bold]Select Number > ").removesuffix(".")

        ## Operations
        match Input:
            case "1": Plus()
            case "2": Minus()
            case "3": Times()
            case "4": Divide()
            case "5": Power()
            case "6": Root()
            case "7": Factorial()
            case "h": Data = ShowHistories(data)
            case "n": WhatsNew()
            case "l" | "exit": return
            case _ :
                Move()
                console.print("[bold red]Invalid command.")
                continue
        
        with console.status("[dim italic]Press enter to continue", spinner="clock"):
            console.input()

        Move()

# Get Data
data_template = {
    "Version" : VERSION, 
    "SaveHistories" : True,
    "Histories" : []
}

data_file = DataHandler("All Data.json", data_template)
Data = data_file.data

# Code
Run(Data)

# Save Data
data_file.save(Data)