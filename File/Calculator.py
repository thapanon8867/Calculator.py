# Calculator.py
# Version 1.11.4
VERSION = [1, 11, 4, None]

# Import things
import math
import time
import os
import json

# Import Rich
try:
    from rich.console import Console
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.table import Table
    from rich.traceback import install as tbinstall
except ModuleNotFoundError:
    print("Please Install rich first")

# Configs
VERSION_MESSAGE = f"Version {VERSION[0]}.{VERSION[1]}.{VERSION[2]} : What's new"
SLEEP_TIME = 1
CLOSE_TIME = 4
VALUEERROR = "Invalid input!: Try again."
ZERODIVISIONERROR = "Cann't divided by zero!\n\n"
ERROR = "An expected error occurred:"

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
def Ask2number() :
    # Ask
    while True :
        try :
            print("\n")

            #Ask A
            a = float(input("A = ").replace(",", ""))
            print(a,"\n")

            #Ask B
            b = float(input("B = ").replace(",", ""))
            print(b,"\n")

            break
        except ValueError :
            print(VALUEERROR)
    
    return a, b

def Ask1number() :
    # Ask
    while True :
        try :
            print("\n")

            #Ask A
            a = float(input("A = ").replace(",", ""))
            print(a,"\n")

            break
        except ValueError :
            print(VALUEERROR)
    
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

        # Show Answer
        time.sleep(SLEEP_TIME)
        print ("Answer =" , Answer ,"\n\n")

        # Save
        if Data["SaveHistories"] == True :
            Data["Histories"].append(f"{a} + {b} = {Answer}")
    except Exception as Reason :
        print(ERROR , Reason)

def Minus() :
    try :
        # Ask
        a, b = Ask2number()
        
        # Calculate
        Answer = a - b

        #Float -> Int
        if Answer == int(Answer) :
            Answer = int(Answer)

        # Show Answer
        time.sleep(SLEEP_TIME)
        print ("Answer =" , Answer ,"\n\n")

        # Save
        if Data["SaveHistories"] == True :
            Data["Histories"].append(f"{a} - {b} = {Answer}")
    
    except Exception as Reason :
        print(ERROR , Reason)

def Times() :
    try :
        # Ask
        a, b = Ask2number()
        
        # Calculate
        Answer = a * b
        
        #Float -> Int
        if Answer == int(Answer) :
            Answer = int(Answer)

        # Show Answer
        time.sleep(SLEEP_TIME)
        print ("Answer =" , Answer ,"\n\n")

        # Save
        if Data["SaveHistories"] == True :
            Data["Histories"].append(f"{a} * {b} = {Answer}")

    except Exception as Reason :
        print(ERROR , Reason)

def Divide() :
    try :
        # Ask
        a, b = Ask2number()
        
        # Calculate
        Answer = int(a // b)
        Remander = int(a % b)
        Answer_WithDecemal = a / b
        
        #Float -> Int & # Show Answer
        time.sleep(SLEEP_TIME)

        if Remander == 0 :
            print ("Answer =" , Answer_WithDecemal ,"\n\n")
        elif Remander != 0 :
            print ("Answer =" , Answer_WithDecemal, "\n")

            if input() == "=" : ## Plus
                time.sleep(SLEEP_TIME)

                print ("\nAnswer =" , Answer)
                print ("Remander =" , Remander ,"\n\n")
                
            

            
        else : raise

        # Save
        if Data["SaveHistories"] == True :
            Data["Histories"].append(f"{a} / {b} = {Answer}")
    except ZeroDivisionError :
        print(ZERODIVISIONERROR)
    except Exception as Reason :
        print("Have Something Error:" , Reason)

def Power() :
    try :
        # Ask
        a, b = Ask2number()
        
        # Calculate
        Answer = math.pow(a,b)
        
        #Float -> Int
        if Answer == int(Answer) :
            Answer = int(Answer)

        # Show Answer
        time.sleep(SLEEP_TIME)
        print ("Answer =" , Answer ,"\n\n")

        # Save
        if Data["SaveHistories"] == True :
            Data["Histories"].append(f"{a} ^ {b} = {Answer}")

    except Exception as Reason :
        print(ERROR , Reason)

def Root() :
    try :
        # Custom Ask
        while True :
            try :
                print("\n")

                #Ask A
                a = input("Sqr, Cqr = ")

                #Check A -> Sqr = True, Cqr = False
                if a == "Sqrt" or a == "2":
                    a = "Sqrt"
                elif a == "Cbrt" or a == "3" :
                    a = "Cbrt"
                else :
                    raise ValueError
                
                print(a,"\n")

                #Ask B
                b = float(input(a+" of "))
                print(b,"\n")

                break
            except ValueError :
                print(VALUEERROR)
        
        # Calculate
        if b <= 0 :
            raise ValueError

        if a == "Sqrt" :
            Answer = math.sqrt(b)
        if a == "Cbrt" :
            Answer = math.pow(b,1/3)
        
        #Float -> Int
        if Answer == int(Answer) :
            Answer = int(Answer)

        # Show Answer
        time.sleep(SLEEP_TIME)
        print ("Answer =" , Answer ,"\n\n")

        # Save
        if Data["SaveHistories"] == True :
            Data["Histories"].append(f"{a} of {b} = {Answer}")

    except ValueError :
        print(f"{VALUEERROR}\n\n")
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

        # Show Answer
        time.sleep(SLEEP_TIME)
        print ("Answer =" , Answer ,"\n\n")

        # Save
        if Data["SaveHistories"] == True :
            Data["Histories"].append(f"{a}! = {Answer}")
    except ValueError :
        print(f"{VALUEERROR}\n\n")
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
            print(f"Error while saving data: File Not Found -- {e}")
        except Exception as e :
            print("Error while saving data:", e)
    
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
def WhatNew() :
    print("")
    print(
        "Version 1.11.0"
        "\n1. Add History System",
        "\n2. Fixed Bug", "\n"
    )
    print(
        "Version 1.11.2",
        "\n1. Add Toggle History System", "\n"
    )
    print(
        "Version 1.11.3"
        "\n1. Delete Manual"
        "\n2. Fixed Bug", "\n"
    )
    print(
        "Version 1.11.4"
        "\n1. Fixed Comma Error",
        "\n2. Fixed Bug\n\n"
    )

def Move() :
    console.clear()

def ShowHistories() :
    global Data

    histories = Data["Histories"]

    # Show
    print("\n--- Calculation Histories ---")

    if len(histories) == 0 :
        print("~~ No history ~~")
    else :
        for i in range(len(histories)) :
            print(histories[i])

    print(f"-----------------------------\nSave History? = {Data["SaveHistories"]}\n-----------------------------")

    # Del?
    AddOn = input("\n")

    if AddOn == "-" : # Clear History
        if input("\nAre you sure you want to clear histories? [y/n]\n= ").lower() == "y" :
            Data["Histories"] = []

            time.sleep(SLEEP_TIME)
            
            print("\nHistories cleared.\n\n")
        else :
            print("\n\n")
    elif AddOn == "0" : # Toggle History
        State = Data["SaveHistories"]
        WillState = not Data["SaveHistories"]

        Data["SaveHistories"] = not Data["SaveHistories"]

        time.sleep(SLEEP_TIME)

        print(f"\n{State} -> {WillState}\n\n")

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
    menu_table.add_row("c.", "Clear Screen")
    menu_table.add_row("h.", "Histories")
    menu_table.add_row("n.", "What's new?")
    menu_table.add_row("l.", "Leave")

    # Return Panel
    menu = Panel(menu_table, title="Menu", expand=False)
    return menu

def Run(HistoriesFile, Data) :
    print(VERSION_MESSAGE)

    while True :
        console.print(getMenuPanel())
        #Input = input("Plus, Minus, Times, Divide, Power, Root, !, Move, Histories, Leave\n= ").strip().lower() ## Guide | Input -> Remove Space -> lower
        Input = console.input("[bold]Select Number > [/]")

        ## Operations
        match Input:
            case "1" | "1.":
                Plus()
            case "2" | "2.":
                Minus()
            case "3" | "3.":
                Times()
            case "4" | "4.":
                Divide()
            case "5" | "5." :
                Power()
            case "6" | "6." :
                Root()
            case "7" | "7." :
                Factorial()
            case "c" | "c." :
                Move()
            case "h" | "h." :
                ShowHistories()
            case "n" | "n." :
                WhatNew()
            case "l" | "l." | "exit" :
                HistoriesFile.save(Data)
                exit()
            case _ :
                print("\nInvalid command.\n\n")

# Code
DataFile = DataHandler("All Data.json")
Data = DataFile.DoFirst(Data)

if Data != None:
    Run(DataFile, Data)
else:
    input("Enter To Leave")