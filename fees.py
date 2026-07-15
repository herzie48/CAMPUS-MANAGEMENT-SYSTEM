import utils
import file_manager

def pay_fees(data):
    """Processes a fee payment for a student and updates the ledger."""
    utils.print_header("Process Fee Payment")
    
    roll = utils.get_valid_roll_number("Enter Student Roll Number: ")
    if roll not in data["students"]:
        utils.print_error("Student roll number not found.")
        return
        
    fees = data["fees"]
    if roll not in fees:
        # If student exists but fee record somehow missing, initialize it
        fees[roll] = {
            "roll_number": roll,
            "total_fees": 50000.0,
            "fees_paid": 0.0,
            "pending_fees": 50000.0
        }
        
    record = fees[roll]
    student_name = data["students"][roll]["name"]
    
    print(f"\nStudent Name: {student_name}")
    print(f"Total Course Fees: ₹{record['total_fees']:.2f}")
    print(f"Fees Paid So Far: ₹{record['fees_paid']:.2f}")
    print(f"Outstanding Balance: ₹{utils.COLOR_RED}{record['pending_fees']:.2f}{utils.COLOR_RESET}")
    
    if record["pending_fees"] == 0:
        utils.print_success("Fees are already fully paid.")
        return
        
    payment = utils.get_valid_float("Enter Amount to Pay: ₹", min_val=1.0, max_val=record["pending_fees"])
    
    # Update payment history
    record["fees_paid"] += payment
    record["pending_fees"] -= payment
    
    file_manager.save_fees(fees)
    utils.print_success(f"Payment of ₹{payment:.2f} processed successfully.")
    
    # Prompt for receipt generation immediately
    receipt = utils.get_valid_choice("Would you like to print a receipt? (Y/N): ", ["Y", "N", "y", "n"]).upper()
    if receipt == "Y":
        generate_receipt_slip(roll, payment, data)

def generate_receipt_slip(roll, amount_paid, data):
    """Helper that renders a styled, printable receipt block in the console."""
    std = data["students"][roll]
    record = data["fees"][roll]
    current_time = utils.get_current_datetime()
    
    width = 50
    print(f"\n{utils.COLOR_CYAN}╔{'═' * (width - 2)}╗")
    print(f"║ {'CAMPUS MANAGEMENT SYSTEM'.center(width - 4)} ║")
    print(f"║ {'OFFICIAL PAYMENT RECEIPT'.center(width - 4)} ║")
    print(f"╠{'═' * (width - 2)}╣")
    print(f"║ Date/Time: {current_time.ljust(width - 15)} ║")
    print(f"║ Roll Number: {roll.ljust(width - 16)} ║")
    print(f"║ Name: {std['name'].ljust(width - 9)} ║")
    print(f"║ Department: {std['department'].ljust(width - 15)} ║")
    print(f"╠{'═' * (width - 2)}╣")
    print(f"║ Amount Paid: ₹{amount_paid:.2f}".ljust(width - 2) + " ║")
    print(f"║ Outstanding Balance: ₹{record['pending_fees']:.2f}".ljust(width - 2) + " ║")
    print(f"║ Status: {'FULLY PAID' if record['pending_fees'] == 0 else 'PARTIALLY PAID'}".ljust(width - 2) + " ║")
    print(f"╚{'═' * (width - 2)}╝{utils.COLOR_RESET}\n")

def view_pending_fees(data):
    """Lists students who have an outstanding balance greater than zero."""
    utils.print_header("Students with Outstanding Dues")
    
    headers = ["Roll No", "Student Name", "Total Fees", "Fees Paid", "Pending Dues", "Phone Number"]
    rows = []
    
    total_pending = 0.0
    
    for roll, fee in data["fees"].items():
        if fee["pending_fees"] > 0:
            name = data["students"][roll]["name"] if roll in data["students"] else "Unknown"
            phone = data["students"][roll]["phone"] if roll in data["students"] else "N/A"
            rows.append([
                roll, name, f"₹{fee['total_fees']:.2f}", 
                f"₹{fee['fees_paid']:.2f}", f"₹{fee['pending_fees']:.2f}", phone
            ])
            total_pending += fee["pending_fees"]
            
    if not rows:
        utils.print_success("Excellent! No pending dues on campus.")
    else:
        utils.print_table(headers, rows)
        print(f"\nTotal Outstanding Collections: {utils.COLOR_RED}₹{total_pending:.2f}{utils.COLOR_RESET}")

def manage_receipt_menu(data):
    """Interactive workflow to print receipts retrospectively."""
    utils.print_header("Generate Student Invoice/Receipt")
    roll = utils.get_valid_roll_number("Enter Student Roll Number: ")
    if roll not in data["students"]:
        utils.print_error("Student roll number not found.")
        return
        
    if roll not in data["fees"]:
        utils.print_warning("No fee ledger exists for this student.")
        return
        
    generate_receipt_slip(roll, 0.0, data)

def fees_menu(data):
    """Sub-menu dashboard for Fee Operations."""
    while True:
        utils.clear_screen()
        options = [
            "1. Process Fee Payment",
            "2. View Outstanding Fee Balances",
            "3. Generate Receipt Slip",
            "4. Back to Main Menu"
        ]
        utils.print_box_menu("Fee Management System", options)
        choice = utils.get_valid_choice("Choose option: ", ["1", "2", "3", "4"])
        
        if choice == "1":
            pay_fees(data)
            utils.pause()
        elif choice == "2":
            view_pending_fees(data)
            utils.pause()
        elif choice == "3":
            manage_receipt_menu(data)
            utils.pause()
        elif choice == "4":
            break
