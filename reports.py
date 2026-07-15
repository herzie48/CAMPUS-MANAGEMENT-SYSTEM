from datetime import datetime
import utils
import file_manager
import marks  # For grade mappings

def generate_student_report(data):
    """Generates an overview report of student metrics, counts, and averages."""
    utils.print_header("Demographic Student Report")
    
    students = data["students"]
    if not students:
        utils.print_info("No students registered.")
        return
        
    total_students = len(students)
    genders = {"Male": 0, "Female": 0, "Other": 0}
    depts = {}
    cgpa_sum = 0.0
    
    headers = ["Roll No", "Name", "Department", "Semester", "CGPA"]
    rows = []
    
    for roll, std in students.items():
        # Update gender count
        g = std["gender"]
        if g in genders:
            genders[g] += 1
            
        # Update department count
        d = std["department"]
        depts[d] = depts.get(d, 0) + 1
        
        # Update CGPA sum
        cgpa_sum += std["cgpa"]
        
        rows.append([roll, std["name"], std["department"], std["semester"], std["cgpa"]])
        
    avg_cgpa = cgpa_sum / total_students
    
    print(f"Total Student Count: {utils.COLOR_CYAN}{total_students}{utils.COLOR_RESET}")
    print(f"Average CGPA on Campus: {utils.COLOR_CYAN}{avg_cgpa:.2f}{utils.COLOR_RESET}")
    print(f"Gender Breakdown: Male ({genders['Male']}) | Female ({genders['Female']}) | Other ({genders['Other']})")
    print(f"Department Breakdown: " + ", ".join([f"{dept} ({cnt})" for dept, cnt in depts.items()]))
    print(f"---------------------------------------------------------------------------------")
    
    utils.print_table(headers, rows)

def generate_attendance_report(data):
    """Generates an attendance audit report for a course."""
    utils.print_header("Course Attendance Audit Report")
    
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course code not found.")
        return
        
    course = data["courses"][code]
    students_list = course["students"]
    attendance = data["attendance"]
    
    if not students_list:
        utils.print_info("No students enrolled in this course.")
        return
        
    headers = ["Roll No", "Student Name", "Present", "Absent", "Total Classes", "Percentage", "Status"]
    rows = []
    
    low_att_count = 0
    
    for roll in students_list:
        name = data["students"][roll]["name"] if roll in data["students"] else "Unknown"
        present = 0
        absent = 0
        
        for (r, c, d), status in attendance.items():
            if r == roll and c == code:
                if status == "P":
                    present += 1
                else:
                    absent += 1
                    
        total = present + absent
        pct = (present / total) * 100.0 if total > 0 else 0.0
        
        if total > 0 and pct < 75.0:
            status_label = f"{utils.COLOR_RED}LOW ATTENDANCE{utils.COLOR_RESET}"
            low_att_count += 1
        elif total == 0:
            status_label = "No Data Logged"
            low_att_count += 1
        else:
            status_label = f"{utils.COLOR_GREEN}OK{utils.COLOR_RESET}"
            
        pct_str = f"{pct:.2f}%" if total > 0 else "0.00%"
        rows.append([roll, name, present, absent, total, pct_str, status_label])
        
    print(f"Course Name: {course['course_name']} ({code})")
    print(f"Enrolled Students count: {len(students_list)}")
    print(f"Students with Warning Flags (< 75%): {utils.COLOR_RED if low_att_count > 0 else utils.COLOR_GREEN}{low_att_count}{utils.COLOR_RESET}")
    print(f"---------------------------------------------------------------------------------")
    
    utils.print_table(headers, rows)

def generate_marks_report(data):
    """Generates an academic performance report for a course."""
    utils.print_header("Course Academic Performance Report")
    
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course code not found.")
        return
        
    course = data["courses"][code]
    students_list = course["students"]
    
    if not students_list:
        utils.print_info("No students enrolled in this course.")
        return
        
    headers = ["Roll No", "Student Name", "Marks Obtained", "Max Marks", "Percentage", "Grade", "Status"]
    rows = []
    
    sum_pct = 0.0
    valid_records = 0
    pass_count = 0
    fail_count = 0
    
    for roll in students_list:
        name = data["students"][roll]["name"] if roll in data["students"] else "Unknown"
        key = (roll, code)
        
        if key in data["marks"]:
            mrk = data["marks"][key]
            obtained = mrk["marks_obtained"]
            mx = mrk["max_marks"]
            pct = (obtained / mx) * 100.0
            grade, gp = marks.get_grade_and_gp(pct)
            
            sum_pct += pct
            valid_records += 1
            
            if pct >= 40.0:
                status = f"{utils.COLOR_GREEN}PASS{utils.COLOR_RESET}"
                pass_count += 1
            else:
                status = f"{utils.COLOR_RED}FAIL{utils.COLOR_RESET}"
                fail_count += 1
                
            rows.append([roll, name, obtained, mx, f"{pct:.2f}%", grade, status])
        else:
            rows.append([roll, name, "N/A", "N/A", "N/A", "N/A", "No Marks Entered"])
            
    print(f"Course Name: {course['course_name']} ({code})")
    if valid_records > 0:
        avg_pct = sum_pct / valid_records
        print(f"Class Average Percentage: {utils.COLOR_CYAN}{avg_pct:.2f}%{utils.COLOR_RESET}")
        print(f"Pass/Fail Summary: Passed {utils.COLOR_GREEN}{pass_count}{utils.COLOR_RESET} | Failed {utils.COLOR_RED}{fail_count}{utils.COLOR_RESET}")
    else:
        print("Class Average Percentage: No grade data available.")
    print(f"---------------------------------------------------------------------------------")
    
    utils.print_table(headers, rows)

def generate_library_report(data):
    """Generates a log of borrowed materials and overdue fines in the library."""
    utils.print_header("Library Borrow Audit Report")
    
    books = data["books"]
    if not books:
        utils.print_info("No books registered in library.")
        return
        
    headers = ["Book ID", "Title", "Author", "Borrowed By", "Student Name", "Due Date", "Fine Status"]
    rows = []
    
    borrowed_total = 0
    overdue_total = 0
    today = datetime.now()
    
    for bid, bk in books.items():
        if bk["borrowed_by"]:
            for roll, due_str in bk["borrowed_by"].items():
                borrowed_total += 1
                name = data["students"][roll]["name"] if roll in data["students"] else "Unknown"
                due_date = datetime.strptime(due_str, "%Y-%m-%d")
                
                if today > due_date:
                    days_overdue = (today - due_date).days
                    fine_accrued = days_overdue * 10.0
                    fine_status = f"{utils.COLOR_RED}OVERDUE (+{days_overdue} days, ₹{fine_accrued:.2f}){utils.COLOR_RESET}"
                    overdue_total += 1
                else:
                    fine_status = f"{utils.COLOR_GREEN}ON TIME{utils.COLOR_RESET}"
                    
                rows.append([bid, bk["title"], bk["author"], roll, name, due_str, fine_status])
                
    print(f"Total Unique Titles in Inventory: {len(books)}")
    print(f"Active Borrowed Copies Count: {utils.COLOR_CYAN}{borrowed_total}{utils.COLOR_RESET}")
    print(f"Overdue Returns Count: {utils.COLOR_RED if overdue_total > 0 else utils.COLOR_GREEN}{overdue_total}{utils.COLOR_RESET}")
    print(f"---------------------------------------------------------------------------------")
    
    utils.print_table(headers, rows)

def generate_fees_report(data):
    """Generates accounting metrics of fees paid vs outstanding balances on campus."""
    utils.print_header("Campus Financial Audit Report")
    
    fees = data["fees"]
    if not fees:
        utils.print_info("No billing ledger records found.")
        return
        
    total_target = 0.0
    total_collected = 0.0
    total_pending = 0.0
    cleared_count = 0
    outstanding_count = 0
    
    cleared_rows = []
    outstanding_rows = []
    
    for roll, fee in fees.items():
        name = data["students"][roll]["name"] if roll in data["students"] else "Unknown"
        dept = data["students"][roll]["department"] if roll in data["students"] else "N/A"
        
        total_target += fee["total_fees"]
        total_collected += fee["fees_paid"]
        total_pending += fee["pending_fees"]
        
        row = [roll, name, dept, f"₹{fee['total_fees']:.2f}", f"₹{fee['fees_paid']:.2f}", f"₹{fee['pending_fees']:.2f}"]
        
        if fee["pending_fees"] == 0:
            cleared_rows.append(row)
            cleared_count += 1
        else:
            outstanding_rows.append(row)
            outstanding_count += 1
            
    pct_collected = (total_collected / total_target) * 100.0 if total_target > 0 else 0.0
    
    print(f"Total Collections Target:  ₹{total_target:,.2f}")
    print(f"Total Fees Settled (Paid): {utils.COLOR_GREEN}₹{total_collected:,.2f}{utils.COLOR_RESET}")
    print(f"Total Fees Outstanding:    {utils.COLOR_RED}₹{total_pending:,.2f}{utils.COLOR_RESET}")
    print(f"Settlement Ratio:          {utils.COLOR_CYAN}{pct_collected:.2f}%{utils.COLOR_RESET}")
    print(f"Dues Breakdown:            Dues Settled ({cleared_count}) | Outstanding Balances ({outstanding_count})")
    print(f"---------------------------------------------------------------------------------")
    
    headers = ["Roll No", "Student Name", "Department", "Total Bill", "Paid Amount", "Outstanding Dues"]
    
    if outstanding_rows:
        print(f"\n{utils.COLOR_RED}OUTSTANDING DUES LEDGER:{utils.COLOR_RESET}")
        utils.print_table(headers, outstanding_rows)
        
    if cleared_rows:
        print(f"\n{utils.COLOR_GREEN}SETTLED ACCOUNTS LEDGER:{utils.COLOR_RESET}")
        utils.print_table(headers, cleared_rows)

def reports_menu(data):
    """Sub-menu interface for generating administrative reports."""
    while True:
        utils.clear_screen()
        options = [
            "1. Generate Student Demographic Summary",
            "2. Generate Course Attendance Report",
            "3. Generate Course Marks/Grade Report",
            "4. Generate Library Borrowing & Overdue Audit",
            "5. Generate Fee Collections & Dues Report",
            "6. Back to Main Menu"
        ]
        utils.print_box_menu("Campus Reports Dashboard", options)
        choice = utils.get_valid_choice("Choose option: ", ["1", "2", "3", "4", "5", "6"])
        
        if choice == "1":
            generate_student_report(data)
            utils.pause()
        elif choice == "2":
            generate_attendance_report(data)
            utils.pause()
        elif choice == "3":
            generate_marks_report(data)
            utils.pause()
        elif choice == "4":
            generate_library_report(data)
            utils.pause()
        elif choice == "5":
            generate_fees_report(data)
            utils.pause()
        elif choice == "6":
            break
