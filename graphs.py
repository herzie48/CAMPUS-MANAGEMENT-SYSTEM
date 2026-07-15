import matplotlib.pyplot as plt
import numpy as np
import utils

def plot_attendance_statistics(data):
    """Generates a line graph showing the daily attendance count trend line for a course."""
    utils.print_header("Generate Attendance Trend Graph")
    
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course code not found.")
        return
        
    attendance = data["attendance"]
    
    # Group attendance by date for this course
    dates_map = {}
    for (r, c, d), status in attendance.items():
        if c == code:
            if d not in dates_map:
                dates_map[d] = {"present": 0, "total": 0}
            dates_map[d]["total"] += 1
            if status == "P":
                dates_map[d]["present"] += 1
                
    if not dates_map:
        utils.print_info("No attendance logs found for this course.")
        return
        
    # Sort dates chronologically
    sorted_dates = sorted(dates_map.keys())
    present_percentages = []
    
    for d in sorted_dates:
        stats = dates_map[d]
        pct = (stats["present"] / stats["total"]) * 100.0
        present_percentages.append(pct)
        
    # Create plot
    plt.figure(figsize=(10, 5))
    plt.plot(sorted_dates, present_percentages, marker='o', linestyle='-', color='teal', linewidth=2)
    plt.title(f"Daily Attendance Trend - {data['courses'][code]['course_name']} ({code})")
    plt.xlabel("Date")
    plt.ylabel("Attendance Percentage (%)")
    plt.ylim(0, 105)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    utils.print_success("Displaying Attendance Trend Line Graph...")
    plt.show()

def plot_marks_distribution(data):
    """Generates a histogram showcasing student marks distribution for a course."""
    utils.print_header("Generate Marks Distribution Histogram")
    
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course code not found.")
        return
        
    marks_list = []
    for (roll, c), mrk in data["marks"].items():
        if c == code:
            pct = (mrk["marks_obtained"] / mrk["max_marks"]) * 100.0
            marks_list.append(pct)
            
    if not marks_list:
        utils.print_info("No marks data logged for this course.")
        return
        
    # Plot histogram
    plt.figure(figsize=(8, 5))
    plt.hist(marks_list, bins=5, edgecolor='black', color='skyblue', alpha=0.8)
    plt.title(f"Score Distribution - {data['courses'][code]['course_name']} ({code})")
    plt.xlabel("Score Percentage (%)")
    plt.ylabel("Number of Students")
    plt.xlim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    utils.print_success("Displaying Marks Distribution Histogram...")
    plt.show()

def plot_department_averages(data):
    """Generates a bar chart showcasing average CGPA per department."""
    utils.print_header("Generate Department CGPA Bar Chart")
    
    students = data["students"].values()
    if not students:
        utils.print_info("No student records found.")
        return
        
    dept_map = {}
    for std in students:
        dept = std["department"]
        if dept not in dept_map:
            dept_map[dept] = []
        dept_map[dept].append(std["cgpa"])
        
    depts = list(dept_map.keys())
    averages = [np.mean(dept_map[d]) for d in depts]
    
    # Create bar chart
    plt.figure(figsize=(9, 5))
    bars = plt.bar(depts, averages, color=['coral', 'dodgerblue', 'mediumseagreen', 'orchid'], edgecolor='black')
    
    plt.title("Average Student CGPA by Department")
    plt.xlabel("Department")
    plt.ylabel("Average CGPA")
    plt.ylim(0, 10.5)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height + 0.2, f"{height:.2f}", ha='center', va='bottom', fontweight='bold')
        
    plt.tight_layout()
    utils.print_success("Displaying Department CGPA Averages Bar Chart...")
    plt.show()

def plot_grade_distribution(data):
    """Generates a pie chart of letter grade distribution (O, A+, A, B+, B, C, F) for a course."""
    utils.print_header("Generate Grade Distribution Pie Chart")
    
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course code not found.")
        return
        
    # Local grades import helper
    import marks
    
    grade_counts = {"O": 0, "A+": 0, "A": 0, "B+": 0, "B": 0, "C": 0, "F": 0}
    total = 0
    
    for (roll, c), mrk in data["marks"].items():
        if c == code:
            pct = (mrk["marks_obtained"] / mrk["max_marks"]) * 100.0
            grade_full, gp = marks.get_grade_and_gp(pct)
            # Extract first grade letter token e.g. "O" or "A+"
            grade_letter = grade_full.split(" ")[0]
            if grade_letter in grade_counts:
                grade_counts[grade_letter] += 1
                total += 1
                
    if total == 0:
        utils.print_info("No grading records logged for this course.")
        return
        
    labels = []
    sizes = []
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'orange', 'plum', 'red']
    
    for g, count in grade_counts.items():
        if count > 0:
            labels.append(f"Grade {g} ({count})")
            sizes.append(count)
            
    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, colors=colors[:len(labels)], autopct='%1.1f%%', startangle=140, shadow=True)
    plt.title(f"Grade Letter Distribution - {data['courses'][code]['course_name']} ({code})")
    plt.tight_layout()
    utils.print_success("Displaying Grade Distribution Pie Chart...")
    plt.show()

def plot_fee_collection(data):
    """Generates a pie chart displaying total paid fees vs outstanding fees on campus."""
    utils.print_header("Generate Fee Collection Summary Pie Chart")
    
    fees = data["fees"].values()
    if not fees:
        utils.print_info("No fee records logged in the database.")
        return
        
    total_paid = sum(fee["fees_paid"] for fee in fees)
    total_pending = sum(fee["pending_fees"] for fee in fees)
    
    if total_paid == 0 and total_pending == 0:
        utils.print_info("No fee values set yet.")
        return
        
    labels = [f"Paid Fees (₹{total_paid:,.2f})", f"Pending Fees (₹{total_pending:,.2f})"]
    sizes = [total_paid, total_pending]
    colors = ['mediumseagreen', 'crimson']
    
    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, explode=(0.05, 0))
    plt.title("Campus Fee Collection Accounting Summary")
    plt.tight_layout()
    utils.print_success("Displaying Fee Collection Pie Chart...")
    plt.show()

def plot_library_statistics(data):
    """Generates a bar chart displaying borrowing frequency for each book."""
    utils.print_header("Generate Library Borrowing Statistics Bar Chart")
    
    books = data["books"].values()
    if not books:
        utils.print_info("No book records registered.")
        return
        
    titles = []
    borrow_counts = []
    
    for bk in books:
        titles.append(bk["title"])
        borrow_counts.append(len(bk["borrowed_by"]))
        
    if sum(borrow_counts) == 0:
        utils.print_info("No books are currently borrowed by any student.")
        return
        
    # Plot bar chart
    plt.figure(figsize=(10, 5))
    bars = plt.bar(titles, borrow_counts, color='mediumpurple', edgecolor='black')
    plt.title("Library Books Current Borrowing Frequencies")
    plt.xlabel("Book Title")
    plt.ylabel("Active Borrow Copies Count")
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.xticks(rotation=30, ha='right')
    
    # Set y-axis integers
    plt.yticks(np.arange(0, max(borrow_counts) + 2, 1))
    
    plt.tight_layout()
    utils.print_success("Displaying Library Borrowing Bar Chart...")
    plt.show()

def graphs_menu(data):
    """Sub-menu interface for charting visualizations."""
    while True:
        utils.clear_screen()
        options = [
            "1. Plot Attendance Trend Graph (Line Graph)",
            "2. Plot Marks Distribution (Histogram)",
            "3. Plot Department CGPA Averages (Bar Chart)",
            "4. Plot Course Grade Distribution (Pie Chart)",
            "5. Plot Fee Collection Balance (Pie Chart)",
            "6. Plot Library Borrowing Popularity (Bar Chart)",
            "7. Back to Main Menu"
        ]
        utils.print_box_menu("Matplotlib Visualization Center", options)
        choice = utils.get_valid_choice("Choose option: ", ["1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "1":
            plot_attendance_statistics(data)
            utils.pause()
        elif choice == "2":
            plot_marks_distribution(data)
            utils.pause()
        elif choice == "3":
            plot_department_averages(data)
            utils.pause()
        elif choice == "4":
            plot_grade_distribution(data)
            utils.pause()
        elif choice == "5":
            plot_fee_collection(data)
            utils.pause()
        elif choice == "6":
            plot_library_statistics(data)
            utils.pause()
        elif choice == "7":
            break
