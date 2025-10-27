"""
inventory_system.py

A simple inventory management system script for Lab 5.
Handles adding, removing, and reporting stock items.
"""
# FIX (F401/W0611): Removed unused 'import logging'
import json
from datetime import datetime

# Global variable
stock_data = {}


# FIX (C0103): Renamed all functions to snake_case
# FIX (C0116): Added docstrings to all functions
def add_item(item="default", qty=0, logs=None):
    """
    Adds a specified quantity of an item to the stock.
    Logs the transaction to a provided list.
    """
    # FIX (W0102): Changed mutable default logs=[] to None
    if logs is None:
        logs = []

    if not item:
        return

    # FIX (Runtime TypeError): Added type checking for quantity
    if not isinstance(qty, (int, float)):
        print(f"Error: Quantity '{qty}' for item '{item}' is not a number. Skipping.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    
    # FIX (C0209): Converted string formatting to an f-string
    logs.append(f"{str(datetime.now())}: Added {qty} of {item}")


def remove_item(item, qty):
    """
    Removes a specified quantity of an item from the stock.
    Deletes the item if its stock reaches 0 or less.
    """
    # FIX (E722/W0702/B110): Replaced bare 'except:' with 'except KeyError:'
    try:
        if stock_data[item] <= qty:
            del stock_data[item]
        else:
            stock_data[item] -= qty
    except KeyError:
        # Added a helpful message instead of 'pass'
        print(f"Warning: Tried to remove item '{item}' which does not exist.")


def get_qty(item):
    """Returns the quantity of a specific item in stock."""
    # FIX (Bug): Used .get() to prevent crash if item doesn't exist
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Loads the inventory data from a JSON file."""
    # FIX (W0603): 'global' is needed here, but we can make the function safer
    global stock_data
    
    # FIX (R1732): Used 'with' to open files safely
    # FIX (W1514): Added 'encoding="utf-8"'
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.loads(f.read())
    except FileNotFoundError:
        print(f"Warning: {file} not found. Starting with empty inventory.")
        stock_data = {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode {file}. Starting with empty inventory.")
        stock_data = {}


def save_data(file="inventory.json"):
    """Saves the current inventory data to a JSON file."""
    # FIX (R1732): Used 'with' to open files safely
    # FIX (W1514): Added 'encoding="utf-8"'
    with open(file, "w", encoding="utf-8") as f:
        # Added indent=4 for a human-readable JSON file
        f.write(json.dumps(stock_data, indent=4))


def print_data():
    """Prints a formatted report of all items and their quantities."""
    print("\n--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    else:
        for item, qty in stock_data.items():
            print(f"{item} -> {qty}")
    print("--------------------\n")


def check_low_items(threshold=5):
    """Returns a list of items with stock below the threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Main function to run the inventory operations."""
    load_data()  # Load data at the start
    
    # FIX (C0103): Updated all function calls to snake_case
    add_item("apple", 10)
    add_item("banana", 20)
    
    # This call is now safely handled by type checking in add_item
    add_item(123, "ten")  
    
    remove_item("apple", 3)
    
    # This call is now safely handled by the 'except KeyError'
    remove_item("orange", 1)

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    
    print_data()
    save_data()
    
    # FIX (W0123/B307): Removed dangerous 'eval()' call
    print("Log: 'eval' call removed for security.")


# FIX (E305): Added 2 blank lines before this call
if __name__ == "__main__":
    main()