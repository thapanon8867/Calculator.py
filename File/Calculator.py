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
IMAGINARYERROR = "[bold red]ImaginaryError:"
ERROR = "[bold red]An expected error occurred:"

tbinstall(); del tbinstall
console = Console()
layout = Layout()

# Custom Errors
class VersionError(Exception): pass
class ImaginaryError(Exception): pass

def debug(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, ValueError): console.print(VALUEERROR)
            elif isinstance(e, ZeroDivisionError): console.print(ZERODIVISIONERROR)
            elif isinstance(e, OverflowError): console.print(OVERFLOWERROR)
            elif isinstance(e,ImaginaryError): console.print(IMAGINARYERROR, e)
            else: console.print(ERROR, e)
    return wrapper

# Center Functions
@debug
def Ask2number(Aprompt="A? > ", Bprompt="B? > ") :
    #Ask A
    a = float(console.input(f"[bold dim]{Aprompt}").replace(",", ""))
    #Ask B
    b = float(console.input(f"[bold dim]{Bprompt}").replace(",", ""))

    return a, b

@debug
def Ask1number(Aprompt="A? > ") :
    #Ask A
    a = float(console.input(f"[bold dim]{Aprompt}").replace(",", ""))

    return a

@debug
def processOperation(
        format_str: str,
        *op_func,
        mode: int = 2,
        Aprompt: str = "A? > ",
        Bprompt: str = "B? > ",
        answer_messages: tuple = ["Answer"],
        safety_func = None
) -> None:

    a, b = 0, 0

    if mode == 1: a = Ask1number(Aprompt)
    else: a, b = Ask2number(Aprompt, Bprompt); mode = 2

    if safety_func and mode == 2: safety_func(a, b) # Do safely
    elif safety_func and mode == 1: safety_func(a)

    with console.status("[bold green]Thinking..."):
        # Finding Answer(s)
        answers = []
        for func in op_func: # Loop for all method
            # Do the method
            if mode == 2: answer = func(a, b)
            elif mode == 1: answer = func(a)

            if isinstance(answer, float) and answer.is_integer(): answer = int(answer) # If can int then int
            answers.append(answer)
        
        # Saving
        if Data["SaveHistories"]:
            save_msg = format_str.format(a, b, answers[0])
            Data["Histories"].append(save_msg)
        
        time.sleep(SLEEP_TIME)
    # Printing Answer(s)
    for i, msg in enumerate(answer_messages): # i <- index | msg <- answer_message <- answer_messages
        style = "bold yellow" if i == 0 else "dim yellow"
        console.print(f"[{style}]{msg} = {answers[i]}")

# Operator Functions
def Plus() :
    processOperation("{0} + {1} = {2}", lambda a, b: a + b)

def Minus() :
    processOperation("{0} - {1} = {2}", lambda a, b: a - b)

def Times() :
    processOperation("{0} * {1} = {2}", lambda a, b: a * b)

def Divide() :
    processOperation("{0} / {1} = {2}", lambda a, b: a / b, lambda a, b: a % b, answer_messages=[
        "Answer",
        "Remainder"
    ])

def Power() :
    processOperation("{0} ^ {1} = {2}", lambda a, b: a ** b, Bprompt="Power of ")

def Root() :
    def logic(n, a):
        if n == 0: raise ZeroDivisionError("Root index cannot be zero.")
        if n % 2 == 0 and a < 0: raise ImaginaryError("Even root of negative number results in complex number (i).")
        if a == 0 and n < 0: raise ZeroDivisionError("Zero cannot be raised to a negative power.")
    processOperation("{1} ^ (1/{0}) = {2}", lambda n, a: a ** (1/n), Aprompt="n? > ", Bprompt="A? > ", safety_func=logic)

def Factorial() :
    def logic(a:float):
        if a > 1000: raise OverflowError
        if not a.is_integer(): raise ValueError
    processOperation("{0}! = {2}", lambda a: math.factorial(int(a)), mode=1, safety_func=logic)

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

data_template = {
    "Version" : VERSION, 
    "SaveHistories" : True,
    "Histories" : []
}

# Code
try:
    # Get Data
    data_file = DataHandler("All Data.json", data_template)
    Data = data_file.data

    Run(Data) # Work

    # Save Data
    with console.status("Saving...", spinner="arc"):
        data_file.save(Data)
        time.sleep(SLEEP_TIME)
except KeyboardInterrupt:
    console.print("[bold red]The program is closing suddenly... Saving data.")
    if "Data" in locals(): data_file.save(Data) # Save