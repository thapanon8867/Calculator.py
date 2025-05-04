import os
import json

# Checking
DataDirPath = os.path.dirname(__file__)
DataDirName = os.path.basename(DataDirPath)

def process(dataDirPath):
    allData = os.path.join(dataDirPath,"All Data.json")

    # Load
    with open(allData, "r") as file:
        data = json.load(file)
        if data["Version"] != [1, 11, 3, None]:
            raise ValueError
        
        data["Version"] = [1, 14, 4, None]
    
    # Write
    with open(allData, "w") as file:
        json.dump(data,  file, indent=4)

try:
    if DataDirName != "Data":
        raise FileExistsError("Code1")
    
    process(DataDirPath)

    print("\nUpdate Data File Successfully (Please replace your calculator.py with the new version before using calculator.)")

except FileExistsError as e:
    if str(e) == "Code1":
        input("Please move this file to calculator's data directory\nEnter to quit.")
    else:
        raise FileExistsError(e)