import os

def Install():
    pass

def Upgrade():
    pass


while True:
    Mode = input("Python Calculator -- Calculator For Everyone\nSelect Mode: [ Install ] [ Upgrade ]\n= ").strip().lower()

    if Mode in ("install", "ins", "1", "[ install ]", "[install]"):
        Install()
        break
    elif Mode in ("upgrade", "upd", "2", "[ upgrade ]", "[upgrade]"):
        Upgrade()
        break
    else:
        print("\nWrong Value\n")

input("\nProgram Has Installed.\n")