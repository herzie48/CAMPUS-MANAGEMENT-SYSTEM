from datetime import datetime, timedelta
import utils
import file_manager

def add_book(data):
    """Adds a new book or increments the quantity of an existing book in the library."""
    utils.print_header("Add Book to Library")
    books = data["books"]
    
    bid = utils.get_valid_string("Enter Book ID (e.g. B101): ").upper()
    
    if bid in books:
        print(f"Book with ID {bid} already exists ({books[bid]['title']}).")
        add_qty = utils.get_valid_int("Enter quantity to add: ", min_val=1)
        books[bid]["quantity"] += add_qty
        utils.print_success(f"Added {add_qty} more copies. New total quantity: {books[bid]['quantity']}.")
    else:
        title = utils.get_valid_string("Enter Book Title: ")
        author = utils.get_valid_string("Enter Author Name: ")
        qty = utils.get_valid_int("Enter Total Quantity: ", min_val=1)
        
        books[bid] = {
            "book_id": bid,
            "title": title,
            "author": author,
            "quantity": qty,
            "borrowed_by": {}  # roll_number -> due_date (YYYY-MM-DD)
        }
        utils.print_success(f"Book '{title}' added to library successfully.")
        
    file_manager.save_books(books)

def remove_book(data):
    """Removes a book from the library database."""
    utils.print_header("Remove Book from Library")
    books = data["books"]
    
    bid = utils.get_valid_string("Enter Book ID to remove: ").upper()
    if bid not in books:
        utils.print_error("Book not found.")
        return
        
    book = books[bid]
    if book["borrowed_by"]:
        utils.print_warning("Cannot remove book. Some copies are currently borrowed by students.")
        return
        
    confirm = input(f"Are you sure you want to remove '{book['title']}'? (Y/N): ").strip().upper()
    if confirm == "Y":
        del books[bid]
        file_manager.save_books(books)
        utils.print_success("Book deleted successfully.")
    else:
        utils.print_info("Removal cancelled.")

def search_books(data):
    """Searches for books by ID, title, or author."""
    utils.print_header("Search Library Books")
    query = utils.get_valid_string("Enter search term (ID, Title, Author): ").lower()
    
    headers = ["Book ID", "Title", "Author", "Available Stock", "Times Borrowed"]
    rows = []
    
    for bid, bk in data["books"].items():
        if (query in bid.lower() or 
            query in bk["title"].lower() or 
            query in bk["author"].lower()):
            borrowed_count = len(bk["borrowed_by"])
            avail = bk["quantity"] - borrowed_count
            rows.append([bid, bk["title"], bk["author"], f"{avail} / {bk['quantity']}", borrowed_count])
            
    utils.print_table(headers, rows)

def view_all_books(data):
    """Renders a grid displaying all library book records."""
    utils.print_header("Library Catalog")
    headers = ["Book ID", "Title", "Author", "Available Stock", "Times Borrowed"]
    rows = []
    
    for bid, bk in data["books"].items():
        borrowed_count = len(bk["borrowed_by"])
        avail = bk["quantity"] - borrowed_count
        rows.append([bid, bk["title"], bk["author"], f"{avail} / {bk['quantity']}", borrowed_count])
        
    utils.print_table(headers, rows)

def borrow_book(data):
    """Lends a book to a student, validating copy availability and due date assignment."""
    utils.print_header("Borrow Book")
    
    roll = utils.get_valid_roll_number("Enter Student Roll Number: ")
    if roll not in data["students"]:
        utils.print_error("Student roll number not found.")
        return
        
    bid = utils.get_valid_string("Enter Book ID to borrow: ").upper()
    if bid not in data["books"]:
        utils.print_error("Book not found in catalog.")
        return
        
    book = data["books"][bid]
    
    # Check inventory
    borrowed_count = len(book["borrowed_by"])
    if borrowed_count >= book["quantity"]:
        utils.print_error("All copies of this book are currently borrowed.")
        return
        
    # Prevent duplicate borrows of the same book
    if roll in book["borrowed_by"]:
        utils.print_warning(f"Student has already borrowed a copy of this book. Due date: {book['borrowed_by'][roll]}")
        return
        
    # Calculate due date: 14 days from today
    due_date = datetime.now() + timedelta(days=14)
    due_date_str = due_date.strftime("%Y-%m-%d")
    
    # Record transaction
    book["borrowed_by"][roll] = due_date_str
    file_manager.save_books(data["books"])
    
    utils.print_success(f"Book '{book['title']}' borrowed successfully by {data['students'][roll]['name']}.")
    print(f"Please return it by: {utils.COLOR_CYAN}{due_date_str}{utils.COLOR_RESET} to avoid late fines.")

def return_book(data):
    """Processes returned books and computes late return fees (₹10/day)."""
    utils.print_header("Return Book")
    
    roll = utils.get_valid_roll_number("Enter Student Roll Number: ")
    bid = utils.get_valid_string("Enter Book ID to return: ").upper()
    
    if bid not in data["books"]:
        utils.print_error("Book not found.")
        return
        
    book = data["books"][bid]
    if roll not in book["borrowed_by"]:
        utils.print_error("This student did not borrow this book.")
        return
        
    due_date_str = book["borrowed_by"][roll]
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    today = datetime.now()
    
    # Calculate fine
    fine = 0.0
    if today > due_date:
        overdue_days = (today - due_date).days
        fine = overdue_days * 10.0  # ₹10 per day late
        
    # Return book
    del book["borrowed_by"][roll]
    file_manager.save_books(data["books"])
    
    utils.print_success(f"Book '{book['title']}' returned successfully.")
    
    if fine > 0:
        utils.print_warning(f"Book was overdue! Total Days Late: {overdue_days}")
        print(f"Computed Late Fine: {utils.COLOR_RED}₹{fine:.2f}{utils.COLOR_RESET}")
        
        # Charge the fine to student's pending fees account
        if roll in data["fees"]:
            data["fees"][roll]["total_fees"] += fine
            data["fees"][roll]["pending_fees"] += fine
            file_manager.save_fees(data["fees"])
            utils.print_info("Late fine has been added to student's pending fees account.")
    else:
        utils.print_success("Returned on time. No fine charged.")

def library_menu(data):
    """Sub-menu interface for Library operations."""
    while True:
        utils.clear_screen()
        options = [
            "1. Add Book to Inventory",
            "2. Remove Book from Inventory",
            "3. Search Book Catalog",
            "4. View All Books",
            "5. Borrow a Book",
            "6. Return a Book",
            "7. Back to Main Menu"
        ]
        utils.print_box_menu("Library Management", options)
        choice = utils.get_valid_choice("Choose option: ", ["1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "1":
            add_book(data)
            utils.pause()
        elif choice == "2":
            remove_book(data)
            utils.pause()
        elif choice == "3":
            search_books(data)
            utils.pause()
        elif choice == "4":
            view_all_books(data)
            utils.pause()
        elif choice == "5":
            borrow_book(data)
            utils.pause()
        elif choice == "6":
            return_book(data)
            utils.pause()
        elif choice == "7":
            break
