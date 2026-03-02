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
ERROR = "[bold red]An expected error occurred:"

tbinstall(); del tbinstall
console = Console()
layout = Layout()

# DataFile
Data = {
    "Version" : VERSION, 
    "SaveHistories" : True,
    "Histories" : []
}

# Number Functions
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

# Operator Functions
def Plus() :
    try :
        # Ask
        a, b = Ask2number()
        # Calculate
        Answer = a + b
        #Float -> Int
        if Answer == int(Answer) :
            Answer = int(Answer)

        with console.status("[bold green]Thinking...") as _:
            # Save
            if Data["SaveHistories"] == True :
                Data["Histories"].append(f"{a} + {b} = {Answer}")
            # Show Answer
            time.sleep(SLEEP_TIME)
        console.print(f"[bold yellow]Answer = {Answer}")
    except Exception as Reason :
        console.print(ERROR , Reason)

def Minus() :
    try :
        # Ask
        a, b = Ask2number()
        # Calculate
        Answer = a - b
        #Float -> Int
        if Answer == int(Answer):
            Answer = int(Answer)

        with console.status("[bold green]Thinking...") as _:
            # Save
            if Data["SaveHistories"] == True :
                Data["Histories"].append(f"{a} - {b} = {Answer}")
            # Show Answer
            time.sleep(SLEEP_TIME)
        console.print(f"[bold yellow]Answer = {Answer}")
    except Exception as Reason :
        console.print(ERROR , Reason)

def Times() :
    try:
        # Ask
        a, b = Ask2number()
        # Calculate
        Answer = a * b
        #Float -> Int
        if Answer == int(Answer) :
            Answer = int(Answer)

        with console.status("[bold green]Thinking...") as _:
            # Save
            if Data["SaveHistories"] == True :
                Data["Histories"].append(f"{a} * {b} = {Answer}")
            # Show Answer
            time.sleep(SLEEP_TIME)
        console.print(f"[bold yellow]Answer = {Answer}")
    except Exception as Reason :
        console.print(ERROR , Reason)

def Divide() :
    try :
        # Ask
        a, b = Ask2number()
        # Calculate
        Answer = a / b
        Remander = int(a % b)
        
        with console.status("[bold green]Thinking...") as _:
            # Save
            if Data["SaveHistories"] == True :
                Data["Histories"].append(f"{a} / {b} = {Answer}")
            # Show Answer
            time.sleep(SLEEP_TIME)
            console.print(f"[bold yellow]Answer = {Answer}")
            console.print(f"[dim yellow]Remander = {Remander}")
    except ZeroDivisionError :
        console.print(ZERODIVISIONERROR)
    except Exception as Reason :
        console.print(ERROR , Reason)

def Power() :
    try :
        # Ask
        a, b = Ask2number(Bprompt="Power of ")
        # Calculate
        Answer = a ** b
        #Float -> Int
        if Answer == int(Answer) :
            Answer = int(Answer)

        with console.status("[bold green]Thinking...") as _:
            # Save
            if Data["SaveHistories"] == True :
                Data["Histories"].append(f"{a} ^ {b} = {Answer}")
            # Show Answer
            time.sleep(SLEEP_TIME)
            console.print(f"[bold yellow]Answer = {Answer}")

    except Exception as Reason :
        console.print(ERROR , Reason)

def Root() :
    try :
        # Ask
        console.print("[bold green]nth root of a number")
        n, a = Ask2number("n? > ", "a? > ")
        # Calculate
        if a <= 0 and a % 2 != 0 and n <= 0: raise ValueError
        Answer = a ** (1/n)
        #Float -> Int
        if Answer == int(Answer) :
            Answer = int(Answer)

        with console.status("[bold green]Thinking...") as _:
            # Save
            if Data["SaveHistories"] == True :
                Data["Histories"].append(f"{a} ^ ({1}/{n}) = {Answer}")
            # Show Answer
            time.sleep(SLEEP_TIME)
            console.print(f"[bold yellow]Answer = {Answer}")
    except ValueError :
        console.print(VALUEERROR)
    except Exception as Reason :
        print(ERROR , Reason)

def Factorial() :
    try :
        # Ask
        a = Ask1number()
        if int(a) != a or math.fabs(a) != a:
            raise ValueError
        # Calculate
        Answer = math.factorial(int(a))

        with console.status("[bold green]Thinking...") as _:
            # Save
            if Data["SaveHistories"] == True :
                Data["Histories"].append(f"{a}! = {Answer}")
            # Show Answer
            time.sleep(SLEEP_TIME)
        console.print(f"[bold yellow]Answer = {Answer}")
    except ValueError :
        console.print(VALUEERROR)
    except Exception as Reason :
        print(ERROR , Reason)

# Save Class
class DataHandler :
    Address_script = os.path.abspath(__file__)
    Address_scriptFolder = os.path.dirname(Address_script)
    Address_dataCenter = os.path.join(Address_scriptFolder, "Data")
    
      
    def __init__(self, file_name:str) :
        # Save File Name
        self.__file_name = file_name
        self.__Address_file = os.path.join(self.Address_dataCenter, self.__file_name)

        # Check Folder
        if not os.path.exists(self.Address_dataCenter) :
            os.mkdir(self.Address_dataCenter)
        
        # Check File
        if os.path.exists(self.__Address_file) :
            self.EverExists = True
        else :
            self.EverExists = False
            
    def save(self, data) :
        try :
            if data != None:
                with open(self.__Address_file, "w") as file :
                    json.dump(data, file, indent=4) # Push
        except FileNotFoundError as e:
            console.print(f"[bold red]Error while saving data: File Not Found [/]-- {e}")
        except Exception as e :
            console.print("[bold red]Error while saving data:", e)
    
    def get(self) :
        try :
            with open(self.__Address_file,"r") as file :
                data = json.load(file) # Pull

            if data["Version"] != VERSION:
                raise FileNotFoundError("Wrong Version -- Please Update Your Data First")

            return data # Send
        except FileNotFoundError as e:
            print(f"Error while geting data: File Not Found -- {e} -- Then restart the program.")
            return None
        except Exception as e :
            print("Error while geting data:", e)

    def DoFirst(self, EmptyData) :
        if self.EverExists == False :
            self.save(EmptyData)
            return EmptyData
        else :
            return self.get()

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

def ShowHistories() :
    global Data

    histories = Data["Histories"]

    hisTable = Table(box=None, show_header=False)

    if len(histories) == 0 :
        hisTable.add_row(Align.center("[bold yellow]~~ No history ~~"))
    else :
        for i in range(len(histories)) :
            hisTable.add_row(histories[i])

    hisPanel = Panel(hisTable, title="[bold]Calculation Histories", expand=False)
    console.print(hisPanel)
    if Data["SaveHistories"]: console.print(f"[bold][cyan]Save History? = [/cyan][green]{Data["SaveHistories"]}")
    else: console.print(f"[bold][cyan]Save History? = [/cyan][red]{Data["SaveHistories"]}")

    # Del?
    Input = console.input("[bold]Do you want to clear histories? \\[y/N]    ").lower()
    if Input == "y":
        with console.status("[bold green]Working...") as _: # Make Loading
            Data["Histories"] = []
            time.sleep(SLEEP_TIME)
        console.print("    [bold yellow]Histories cleared.")
    
    # Toggle?
    Input = console.input("[bold]Toggle histories? \\[y/N]    ").lower()
    if Input == "y":
        with console.status("[bold green]Working...") as _:
            Data["SaveHistories"] = not Data["SaveHistories"]
            time.sleep(SLEEP_TIME)
        code = "green" if Data["SaveHistories"] else "red"
        ncode = "red" if Data["SaveHistories"] else "green"
        console.print(f"    [bold][yellow]Toggled from [/yellow][{ncode}]{not Data["SaveHistories"]}[/{ncode}] -> [{code}]{Data["SaveHistories"]}[/{code}].")

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

def Run(HistoriesFile, Data) :
    Move()
    console.print(f"[bold underline white]{VERSION_MESSAGE}")

    while True :
        console.print(getMenuPanel())
        Input = console.input("[bold]Select Number > ").removesuffix(".")

        ## Operations
        match Input:
            case "1":
                Plus()
            case "2":
                Minus()
            case "3":
                Times()
            case "4":
                Divide()
            case "5":
                Power()
            case "6":
                Root()
            case "7":
                Factorial()
            case "h":
                ShowHistories()
            case "n":
                WhatsNew()
            case "l" | "exit":
                HistoriesFile.save(Data)
                exit()
            case _ :
                console.print("[bold red]Invalid command.")
        
        with console.status("[blink dim]Press enter to continue", spinner="clock"):
            console.input()

        Move()

# Code
DataFile = DataHandler("All Data.json")
Data = DataFile.DoFirst(Data)

if Data != None:
    Run(DataFile, Data)
else:
    console.input("Enter To Leave")