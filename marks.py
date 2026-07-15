import utils
import file_manager

def get_grade_and_gp(percentage):
    """Maps a percentage score to a letter grade and a grade point value.
    
    Returns:
        tuple: (grade_letter, grade_point)
    """
    if percentage >= 90.0:
        return "O (Outstanding)", 10
    elif percentage >= 80.0:
        return "A+ (Excellent)", 9
    elif percentage >= 70.0:
        return "A (Very Good)", 8
    elif percentage >= 60.0:
        return "B+ (Good)", 7
    elif percentage >= 50.0:
        return "B (Above Average)", 6
    elif percentage >= 40.0:
        return "C (Pass)", 5
    else:
        return "F (Fail)", 0

def add_marks(data):
    """Logs course marks for an enrolled student."""
    utils.print_header("Add Marks Record")
    
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course code not found.")
        return
        
    course = data["courses"][code]
    
    roll = utils.get_valid_roll_number("Enter Student Roll Number: ")
    if roll not in data["students"]:
        utils.print_error("Student roll number not found.")
        return
        
    if roll not in course["students"]:
        utils.print_error(f"Student {data['students'][roll]['name']} ({roll}) is not enrolled in course {code}.")
        return
        
    marks = data["marks"]
    key = (roll, code)
    if key in marks:
        utils.print_warning(f"Marks for student {roll} in course {code} already exist. Use edit options to change them.")
        return
        
    max_marks = utils.get_valid_float("Enter Maximum Marks: ", min_val=1.0, max_val=200.0)
    obtained = utils.get_valid_float("Enter Marks Obtained: ", min_val=0.0, max_val=max_marks)
    
    marks[key] = {
        "roll_number": roll,
        "course_code": code,
        "marks_obtained": obtained,
        "max_marks": max_marks
    }
    
    file_manager.save_marks(marks)
    utils.print_success("Marks recorded successfully.")

def edit_marks(data):
    """Updates existing marks entries."""
    utils.print_header("Edit Marks Record")
    
    roll = utils.get_valid_roll_number("Enter Student Roll Number: ")
    code = utils.get_valid_string("Enter Course Code: ").upper()
    
    marks = data["marks"]
    key = (roll, code)
    
    if key not in marks:
        utils.print_error("No marks record found for this combination.")
        return
        
    mrk = marks[key]
    print(f"Current Marks: {mrk['marks_obtained']} / {mrk['max_marks']}")
    
    max_marks = utils.get_valid_float("Enter New Maximum Marks: ", min_val=1.0, max_val=200.0)
    obtained = utils.get_valid_float("Enter New Marks Obtained: ", min_val=0.0, max_val=max_marks)
    
    mrk["marks_obtained"] = obtained
    mrk["max_marks"] = max_marks
    
    file_manager.save_marks(marks)
    utils.print_success("Marks record updated.")

def delete_marks(data):
    """Removes a marks entry from the registry."""
    utils.print_header("Delete Marks Record")
    
    roll = utils.get_valid_roll_number("Enter Student Roll Number: ")
    code = utils.get_valid_string("Enter Course Code: ").upper()
    
    marks = data["marks"]
    key = (roll, code)
    
    if key not in marks:
        utils.print_error("No marks record found for this combination.")
        return
        
    confirm = input("Are you sure you want to delete this record? (Y/N): ").strip().upper()
    if confirm == "Y":
        del marks[key]
        file_manager.save_marks(marks)
        utils.print_success("Marks record deleted.")
    else:
        utils.print_info("Deletion cancelled.")

def calculate_subject_topper(data):
    """Finds and displays the student with the highest percentage in a course."""
    utils.print_header("Subject Topper")
    
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course code not found.")
        return
        
    topper_roll = None
    highest_pct = -1.0
    topper_obtained = 0
    topper_max = 0
    
    for (roll, c), mrk in data["marks"].items():
        if c == code:
            pct = (mrk["marks_obtained"] / mrk["max_marks"]) * 100
            if pct > highest_pct:
                highest_pct = pct
                topper_roll = roll
                topper_obtained = mrk["marks_obtained"]
                topper_max = mrk["max_marks"]
                
    if topper_roll is None:
        utils.print_info("No grades have been entered for this course yet.")
    else:
        student_name = data["students"][topper_roll]["name"]
        print(f"\nCourse: {data['courses'][code]['course_name']} ({code})")
        print(f"Subject Topper: {utils.COLOR_GREEN}{student_name} ({topper_roll}){utils.COLOR_RESET}")
        print(f"Marks: {topper_obtained} / {topper_max} ({highest_pct:.2f}%)")

def calculate_overall_topper(data):
    """Finds and displays the student with the highest CGPA."""
    utils.print_header("Overall Topper")
    
    students = data["students"]
    if not students:
        utils.print_info("No students registered.")
        return
        
    topper_roll = None
    highest_cgpa = -1.0
    
    for roll, std in students.items():
        if std["cgpa"] > highest_cgpa:
            highest_cgpa = std["cgpa"]
            topper_roll = roll
            
    if topper_roll:
        std = students[topper_roll]
        print(f"Highest CGPA Student on Campus:")
        print(f"Name: {utils.COLOR_GREEN}{std['name']}{utils.COLOR_RESET}")
        print(f"Roll Number: {std['roll_number']}")
        print(f"Department: {std['department']}")
        print(f"CGPA: {utils.COLOR_CYAN}{std['cgpa']}{utils.COLOR_RESET}")
    else:
        utils.print_warning("Could not calculate topper.")

def view_rank_list(data):
    """Renders a ranked list of students ordered by CGPA descending."""
    utils.print_header("Overall Student Rank List")
    
    students = list(data["students"].values())
    if not students:
        utils.print_info("No student records exist.")
        return
        
    # Sort students descending by CGPA
    ranked = sorted(students, key=lambda x: x["cgpa"], reverse=True)
    
    headers = ["Rank", "Roll No", "Student Name", "Department", "Semester", "CGPA"]
    rows = []
    
    for index, std in enumerate(ranked):
        rows.append([
            index + 1, std["roll_number"], std["name"], 
            std["department"], std["semester"], std["cgpa"]
        ])
        
    utils.print_table(headers, rows)

def view_student_report_card(data):
    """Renders a comprehensive report card showing grade mapping for a selected student."""
    utils.print_header("View Student Report Card")
    
    roll = utils.get_valid_roll_number("Enter Student Roll Number: ")
    if roll not in data["students"]:
        utils.print_error("Student not found.")
        return
        
    std = data["students"][roll]
    print(f"\nStudent Name: {std['name']} | Roll No: {roll} | Dept: {std['department']} | CGPA: {std['cgpa']}")
    
    headers = ["Course Code", "Course Name", "Marks Obtained", "Max Marks", "Percentage", "Grade", "Grade Point"]
    rows = []
    
    total_gp = 0
    total_courses = 0
    
    for (r, c), mrk in data["marks"].items():
        if r == roll:
            course_name = data["courses"][c]["course_name"] if c in data["courses"] else "Unknown"
            pct = (mrk["marks_obtained"] / mrk["max_marks"]) * 100
            grade, gp = get_grade_and_gp(pct)
            rows.append([c, course_name, mrk["marks_obtained"], mrk["max_marks"], f"{pct:.2f}%", grade, gp])
            total_gp += gp
            total_courses += 1
            
    if total_courses == 0:
        utils.print_info("No marks data logged for this student.")
    else:
        utils.print_table(headers, rows)
        gpa = total_gp / total_courses
        print(f"\nTotal Graded Courses: {total_courses} | Computed Semester GPA: {utils.COLOR_CYAN}{gpa:.2f}{utils.COLOR_RESET}")

def marks_menu(data):
    """Sub-menu interface for grading / marks management."""
    while True:
        utils.clear_screen()
        options = [
            "1. Enter Student Marks",
            "2. Edit Student Marks",
            "3. Delete Student Marks",
            "4. View Student Report Card",
            "5. View Course Topper",
            "6. View Overall Topper",
            "7. View Campus Rank List",
            "8. Back to Main Menu"
        ]
        utils.print_box_menu("Examination Management", options)
        choice = utils.get_valid_choice("Choose option: ", ["1", "2", "3", "4", "5", "6", "7", "8"])
        
        if choice == "1":
            add_marks(data)
            utils.pause()
        elif choice == "2":
            edit_marks(data)
            utils.pause()
        elif choice == "3":
            delete_marks(data)
            utils.pause()
        elif choice == "4":
            view_student_report_card(data)
            utils.pause()
        elif choice == "5":
            calculate_subject_topper(data)
            utils.pause()
        elif choice == "6":
            calculate_overall_topper(data)
            utils.pause()
        elif choice == "7":
            view_rank_list(data)
            utils.pause()
        elif choice == "8":
            break
