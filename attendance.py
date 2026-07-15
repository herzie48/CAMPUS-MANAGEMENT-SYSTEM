from datetime import datetime
import utils
import file_manager

def validate_date(date_str):
    """Validates if date_str fits YYYY-MM-DD. Returns True if valid, False otherwise."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_valid_date(prompt, allow_default=True):
    """Prompts for a date, validating format. Defaults to today's date if empty."""
    while True:
        val = input(prompt).strip()
        if not val and allow_default:
            return datetime.now().strftime("%Y-%m-%d")
        if validate_date(val):
            return val
        utils.print_error("Invalid date format. Please use YYYY-MM-DD (e.g. 2026-07-07).")

def mark_attendance(data):
    """Walks through enrolled students of a course on a date and logs attendance."""
    utils.print_header("Mark Attendance")
    
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course code not found.")
        return
        
    course = data["courses"][code]
    students_list = course["students"]
    if not students_list:
        utils.print_warning("No students enrolled in this course yet.")
        return
        
    date = get_valid_date("Enter Date (YYYY-MM-DD) [Press Enter for Today]: ")
    
    print(f"\nMarking attendance for course: {course['course_name']} ({code}) on {date}")
    print("Enter 'P' for Present or 'A' for Absent for each student:\n")
    
    attendance = data["attendance"]
    
    for roll in students_list:
        student_name = data["students"][roll]["name"]
        status = utils.get_valid_choice(f"  {student_name} ({roll}) [P/A]: ", ["P", "A", "p", "a"]).upper()
        attendance[(roll, code, date)] = status
        
    file_manager.save_attendance(attendance)
    utils.print_success(f"Attendance marked successfully for {len(students_list)} students.")

def edit_attendance(data):
    """Updates an individual attendance entry for a student, course, and date."""
    utils.print_header("Edit Attendance Record")
    
    roll = utils.get_valid_roll_number("Enter Student Roll Number: ")
    if roll not in data["students"]:
        utils.print_error("Student roll number not found.")
        return
        
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course code not found.")
        return
        
    date = get_valid_date("Enter Date (YYYY-MM-DD): ", allow_default=False)
    
    attendance = data["attendance"]
    key = (roll, code, date)
    
    if key not in attendance:
        utils.print_warning(f"No existing attendance entry found for {roll} in {code} on {date}.")
        confirm = utils.get_valid_choice("Do you want to create a new entry? (Y/N): ", ["Y", "N", "y", "n"]).upper()
        if confirm == "N":
            return
            
    status = utils.get_valid_choice("Enter Status (P/A): ", ["P", "A", "p", "a"]).upper()
    attendance[key] = status
    file_manager.save_attendance(attendance)
    utils.print_success("Attendance record updated.")

def view_student_attendance(data):
    """Displays attendance logs and percentage for a student in a course."""
    utils.print_header("View Student Attendance Status")
    
    roll = utils.get_valid_roll_number("Enter Student Roll Number: ")
    if roll not in data["students"]:
        utils.print_error("Student not found.")
        return
        
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course not found.")
        return
        
    attendance = data["attendance"]
    
    headers = ["Date", "Status"]
    rows = []
    presents = 0
    total = 0
    
    # Filter attendance records for this student and course
    for (r, c, d), status in attendance.items():
        if r == roll and c == code:
            rows.append([d, status])
            total += 1
            if status == "P":
                presents += 1
                
    if total == 0:
        utils.print_info("No attendance records found for this student in this course.")
        return
        
    # Sort by date
    rows = sorted(rows, key=lambda x: x[0])
    utils.print_table(headers, rows)
    
    percentage = (presents / total) * 100
    color_code = utils.COLOR_GREEN if percentage >= 75.0 else utils.COLOR_RED
    print(f"\nTotal Classes: {total} | Present: {presents} | Absent: {total - presents}")
    print(f"Attendance Percentage: {color_code}{percentage:.2f}%{utils.COLOR_RESET}")

def view_low_attendance_warnings(data):
    """Lists students below 75% attendance for a chosen course."""
    utils.print_header("Low Attendance Warnings (< 75%)")
    
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course not found.")
        return
        
    course = data["courses"][code]
    students_list = course["students"]
    attendance = data["attendance"]
    
    headers = ["Roll No", "Student Name", "Present", "Total Classes", "Percentage"]
    rows = []
    
    for roll in students_list:
        student_name = data["students"][roll]["name"]
        presents = 0
        total = 0
        for (r, c, d), status in attendance.items():
            if r == roll and c == code:
                total += 1
                if status == "P":
                    presents += 1
                    
        if total > 0:
            pct = (presents / total) * 100
            if pct < 75.0:
                rows.append([roll, student_name, presents, total, f"{pct:.2f}%"])
        else:
            # 0 classes attended is 0.00%
            rows.append([roll, student_name, 0, 0, "0.00%"])
            
    if not rows:
        utils.print_success("Great! No students are below 75% attendance in this course.")
    else:
        utils.print_table(headers, rows)

def monthly_attendance_report(data):
    """Generates monthly attendance summary for a course."""
    utils.print_header("Monthly Attendance Report")
    
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course not found.")
        return
        
    month = utils.get_valid_string("Enter Month (YYYY-MM, e.g. 2026-07): ")
    if len(month) != 7 or month[4] != "-":
        utils.print_error("Invalid month format. Please use YYYY-MM.")
        return
        
    course = data["courses"][code]
    students_list = course["students"]
    attendance = data["attendance"]
    
    headers = ["Roll No", "Student Name", "Present", "Absent", "Percentage"]
    rows = []
    
    for roll in students_list:
        student_name = data["students"][roll]["name"]
        presents = 0
        absents = 0
        
        for (r, c, d), status in attendance.items():
            if r == roll and c == code and d.startswith(month):
                if status == "P":
                    presents += 1
                else:
                    absents += 1
                    
        total = presents + absents
        pct_str = f"{(presents / total) * 100:.2f}%" if total > 0 else "N/A"
        rows.append([roll, student_name, presents, absents, pct_str])
        
    utils.print_table(headers, rows)

def attendance_menu(data):
    """Sub-menu dashboard for Attendance Management."""
    while True:
        utils.clear_screen()
        options = [
            "1. Mark Attendance",
            "2. Edit Attendance Record",
            "3. View Student Attendance Percentage",
            "4. View Monthly Attendance Report",
            "5. View Low Attendance Warnings (< 75%)",
            "6. Back to Main Menu"
        ]
        utils.print_box_menu("Attendance Management", options)
        choice = utils.get_valid_choice("Choose option: ", ["1", "2", "3", "4", "5", "6"])
        
        if choice == "1":
            mark_attendance(data)
            utils.pause()
        elif choice == "2":
            edit_attendance(data)
            utils.pause()
        elif choice == "3":
            view_student_attendance(data)
            utils.pause()
        elif choice == "4":
            monthly_attendance_report(data)
            utils.pause()
        elif choice == "5":
            view_low_attendance_warnings(data)
            utils.pause()
        elif choice == "6":
            break
