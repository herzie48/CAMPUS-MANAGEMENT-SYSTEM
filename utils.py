import os
import sys
from datetime import datetime

# ANSI Escape Sequences for Colors
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[91m"      # Errors
COLOR_GREEN = "\033[92m"    # Success
COLOR_YELLOW = "\033[93m"   # Warnings
COLOR_BLUE = "\033[94m"     # Titles / Menus
COLOR_CYAN = "\033[96m"     # Info / Stats
COLOR_BOLD = "\033[1m"

def clear_screen():
    """Clears the console screen in a platform-independent way."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    """Pauses execution and waits for the user to press Enter."""
    print(f"\n{COLOR_YELLOW}Press Enter to continue...{COLOR_RESET}")
    input()

def get_current_datetime():
    """Returns the current date and time formatted as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def print_success(message):
    """Prints a green success message."""
    print(f"{COLOR_GREEN}✔ {message}{COLOR_RESET}")

def print_error(message):
    """Prints a red error message."""
    print(f"{COLOR_RED}✘ Error: {message}{COLOR_RESET}")

def print_warning(message):
    """Prints a yellow warning message."""
    print(f"{COLOR_YELLOW}⚠ Warning: {message}{COLOR_RESET}")

def print_info(message):
    """Prints a cyan information message."""
    print(f"{COLOR_CYAN}ℹ Info: {message}{COLOR_RESET}")

def print_header(title):
    """Prints a styled blue header for sub-menus and sections."""
    width = 60
    print(f"\n{COLOR_BLUE}{'=' * width}")
    print(f"{title.center(width)}")
    print(f"{'=' * width}{COLOR_RESET}\n")

def print_box_menu(title, options):
    """Displays a list of options enclosed in a professional Unicode double-box.
    
    Args:
        title (str): The title of the menu.
        options (list of str): List of options to choose from.
    """
    width = 56
    # Top border
    print(f"{COLOR_BLUE}╔{'═' * (width - 2)}╗")
    
    # Title line
    padded_title = title.center(width - 4)
    print(f"║ {COLOR_BOLD}{padded_title}{COLOR_RESET}{COLOR_BLUE} ║")
    
    # Separator
    print(f"╠{'═' * (width - 2)}╣")
    
    # Menu options
    for option in options:
        # Align options left
        option_line = f"  {option}".ljust(width - 4)
        print(f"║ {COLOR_RESET}{option_line}{COLOR_BLUE} ║")
        
    # Bottom border
    print(f"╚{'═' * (width - 2)}╝{COLOR_RESET}")

def get_valid_string(prompt, allow_empty=False):
    """Prompts user for a string and ensures it's valid (not empty, unless allowed)."""
    while True:
        try:
            val = input(prompt).strip()
            if not allow_empty and not val:
                print_error("Input cannot be empty. Please try again.")
                continue
            return val
        except (KeyboardInterrupt, SystemExit):
            print_error("Operation interrupted.")
            sys.exit(0)

def get_valid_int(prompt, min_val=None, max_val=None):
    """Prompts user for an integer, validating bounds if specified."""
    while True:
        try:
            val_str = input(prompt).strip()
            if not val_str:
                print_error("Input cannot be empty.")
                continue
            val = int(val_str)
            if min_val is not None and val < min_val:
                print_error(f"Value must be at least {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print_error(f"Value must be at most {max_val}.")
                continue
            return val
        except ValueError:
            print_error("Invalid input. Please enter a valid integer.")

def get_valid_float(prompt, min_val=None, max_val=None):
    """Prompts user for a float, validating bounds if specified."""
    while True:
        try:
            val_str = input(prompt).strip()
            if not val_str:
                print_error("Input cannot be empty.")
                continue
            val = float(val_str)
            if min_val is not None and val < min_val:
                print_error(f"Value must be at least {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print_error(f"Value must be at most {max_val}.")
                continue
            return val
        except ValueError:
            print_error("Invalid input. Please enter a valid decimal number.")

def get_valid_choice(prompt, valid_choices):
    """Prompts user for a choice and ensures it's within a list of allowed choices."""
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print_error(f"Invalid option. Allowed choices are: {', '.join(valid_choices)}")

def get_valid_phone(prompt):
    """Validates and returns a phone number (exactly 10 digits)."""
    while True:
        phone = input(prompt).strip()
        if phone.isdigit() and len(phone) == 10:
            return phone
        print_error("Invalid phone number. Must be exactly 10 digits.")

def get_valid_email(prompt):
    """Validates and returns an email address (basic check for '@' and '.')."""
    while True:
        email = input(prompt).strip()
        if "@" in email and "." in email and email.index("@") < email.rindex("."):
            return email
        print_error("Invalid email address. Please include an '@' and a domain (e.g., student@campus.com).")

def get_valid_gender(prompt):
    """Validates and returns gender ('Male', 'Female', 'Other')."""
    while True:
        gender = input(prompt).strip().capitalize()
        if gender in ["Male", "Female", "Other"]:
            return gender
        print_error("Invalid gender. Please enter 'Male', 'Female', or 'Other'.")

def get_valid_roll_number(prompt):
    """Validates and returns a unique alphanumeric roll number."""
    while True:
        roll = input(prompt).strip().upper()
        if roll.isalnum() and len(roll) >= 3:
            return roll
        print_error("Invalid roll number. Must be alphanumeric and at least 3 characters long.")

def print_table(headers, rows):
    """Prints list data as a professional grid table in the console.
    
    Args:
        headers (list of str): Column headers.
        rows (list of list/tuple): Data rows.
    """
    if not rows:
        print_info("No records found to display.")
        return
        
    # Calculate widths based on headers and row data
    widths = [len(h) for h in headers]
    for row in rows:
        for idx, val in enumerate(row):
            widths[idx] = max(widths[idx], len(str(val)))
            
    # Draw horizontal separator
    sep = "+" + "+".join(["-" * (w + 2) for w in widths]) + "+"
    
    print(sep)
    # Header row
    header_str = "|" + "|".join([f" {COLOR_BOLD}{headers[i].ljust(widths[i])}{COLOR_RESET} " for i in range(len(headers))]) + "|"
    print(header_str)
    print(sep)
    
    # Data rows
    for row in rows:
        row_str = "|" + "|".join([f" {str(row[i]).ljust(widths[i])} " for i in range(len(row))]) + "|"
        print(row_str)
        
    print(sep)

