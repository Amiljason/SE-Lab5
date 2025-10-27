import json
# FIX 6: Removed unused 'import logging'
from datetime import datetime

# Global variable
stock_data = {}

# FIX 2: Change mutable default 'logs=[]' to 'logs=None'
def addItem(item="default", qty=0, logs=None):
    # FIX 2: Initialize new list if default is used
    if logs is None:
        logs = []
    
    if not item:
        return
    
    # FIX 1: Add type checking to prevent TypeError
    if not isinstance(qty, (int, float)):
        print(f"Error: Quantity '{qty}' for item '{item}' is not a number. Skipping.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    # Using f-string as suggested by Pylint (C0209)
    logs.append(f"{str(datetime.now())}: Added {qty} of {item}")

def removeItem(item, qty):
    # FIX 4: Specify 'KeyError' instead of using a bare 'except:'
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        # Provide feedback instead of silently passing
        print(f"Warning: Tried to remove item '{item}' which does not exist.")
        pass

def getQty(item):
    return stock_data.get(item, "Item not found") # Use .get() for safety

def loadData(file="inventory.json"):
    # FIX 5: Use 'with' to safely open and close files
    try:
        with open(file, "r") as f:
            global stock_data
            stock_data = json.loads(f.read())
    except FileNotFoundError:
        print(f"Warning: {file} not found. Starting with empty inventory.")
        stock_data = {} # Ensure stock_data is a dict
    except json.JSONDecodeError:
        print(f"Error: Could not decode {file}. Starting with empty inventory.")
        stock_data = {}

def saveData(file="inventory.json"):
    # FIX 5: Use 'with' to safely open and close files
    with open(file, "w") as f:
        f.write(json.dumps(stock_data, indent=4)) # Added indent=4 for readability

def printData():
    print("--- Items Report ---")
    for i in stock_data:
        print(f"{i} -> {stock_data[i]}")
    print("--------------------")

def checkLowItems(threshold=5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    loadData() # Load existing data first
    addItem("apple", 10)
    addItem("banana", 20)
    # This call will now be safely handled by FIX 1
    addItem(123, "ten")
    removeItem("apple", 3)
    # This call will now be safely handled by FIX 4
    removeItem("orange", 1) 
    print(f"Apple stock: {getQty('apple')}")
    print(f"Low items: {checkLowItems()}")
    printData()
    saveData()
    
    # FIX 3: Removed 'eval()' for security
    print("Log: 'eval' call removed for security.")

main()