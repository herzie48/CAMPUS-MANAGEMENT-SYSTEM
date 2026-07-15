import utils
import file_manager

def add_course(data):
    """Adds a new course to the curriculum."""
    utils.print_header("Add Course Record")
    courses = data["courses"]
    
    code = utils.get_valid_string("Enter Course Code (e.g. CS101): ").upper()
    if code in courses:
        utils.print_error(f"Course with code {code} already exists.")
        return
        
    name = utils.get_valid_string("Enter Course Name: ")
    dept = utils.get_valid_string("Enter Department: ")
    credits = utils.get_valid_int("Enter Course Credits (1-6): ", min_val=1, max_val=6)
    
    # Store course details
    courses[code] = {
        "course_code": code,
        "course_name": name,
        "department": dept,
        "credits": credits,
        "faculty_id": "",     # Unassigned initially
        "students": []        # Empty enrollment initially
    }
    file_manager.save_courses(courses)
    utils.print_success(f"Course {name} ({code}) added successfully.")

def delete_course(data):
    """Deletes a course and cascades deletions to faculty assignments, marks, and attendance records."""
    utils.print_header("Delete Course Record")
    courses = data["courses"]
    
    code = utils.get_valid_string("Enter Course Code to delete: ").upper()
    if code not in courses:
        utils.print_error("Course code not found.")
        return
        
    confirm = input(f"Are you sure you want to delete {courses[code]['course_name']} ({code})? (Y/N): ").strip().upper()
    if confirm != 'Y':
        utils.print_info("Deletion cancelled.")
        return
        
    name = courses[code]["course_name"]
    fid = courses[code]["faculty_id"]
    
    # 1. Remove course code from the assigned faculty member's list
    if fid and fid in data["faculty"]:
        if code in data["faculty"][fid]["courses"]:
            data["faculty"][fid]["courses"].remove(code)
            file_manager.save_faculty(data["faculty"])
            
    # 2. Delete all marks associated with this course
    marks = data["marks"]
    marks_keys_to_delete = [k for k in marks.keys() if k[1] == code]
    for k in marks_keys_to_delete:
        del marks[k]
    file_manager.save_marks(marks)
    
    # 3. Delete all attendance associated with this course
    attendance = data["attendance"]
    att_keys_to_delete = [k for k in attendance.keys() if k[1] == code]
    for k in att_keys_to_delete:
        del attendance[k]
    file_manager.save_attendance(attendance)
    
    # 4. Delete course from dictionary
    del courses[code]
    file_manager.save_courses(courses)
    
    utils.print_success(f"Course {name} ({code}) and associated data removed.")

def search_courses(data):
    """Searches courses by code, name, or department."""
    utils.print_header("Search Course Records")
    query = utils.get_valid_string("Enter search term (Code, Name, Dept): ").lower()
    
    headers = ["Course Code", "Course Name", "Department", "Credits", "Faculty ID", "Enrolled Students"]
    rows = []
    
    for code, crs in data["courses"].items():
        if (query in code.lower() or 
            query in crs["course_name"].lower() or 
            query in crs["department"].lower()):
            fid = crs["faculty_id"] if crs["faculty_id"] else "Unassigned"
            student_count = len(crs["students"])
            rows.append([code, crs["course_name"], crs["department"], crs["credits"], fid, student_count])
            
    utils.print_table(headers, rows)

def view_all_courses(data):
    """Renders a table of all existing courses."""
    utils.print_header("All Course Records")
    headers = ["Course Code", "Course Name", "Department", "Credits", "Faculty ID", "Enrolled Students"]
    rows = []
    
    for code, crs in data["courses"].items():
        fid = crs["faculty_id"] if crs["faculty_id"] else "Unassigned"
        student_count = len(crs["students"])
        rows.append([code, crs["course_name"], crs["department"], crs["credits"], fid, student_count])
        
    utils.print_table(headers, rows)

def assign_student_to_course(data):
    """Enrolls a student in a course by roll number."""
    utils.print_header("Enroll Student in Course")
    
    roll = utils.get_valid_roll_number("Enter Student Roll Number: ")
    if roll not in data["students"]:
        utils.print_error("Student roll number not found.")
        return
        
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course code not found.")
        return
        
    course = data["courses"][code]
    if roll in course["students"]:
        utils.print_warning(f"Student {data['students'][roll]['name']} is already enrolled in {course['course_name']}.")
        return
        
    # Enroll student
    course["students"].append(roll)
    file_manager.save_courses(data["courses"])
    utils.print_success(f"Student {data['students'][roll]['name']} enrolled in {course['course_name']} ({code}) successfully.")

def assign_faculty_to_course_wrapper(data):
    """Delegates course assignment workflow to faculty module to maintain code styling and reuse."""
    import faculty
    faculty.assign_faculty_to_course(data)

def course_management_menu(data):
    """Nested menu for Course Management."""
    while True:
        utils.clear_screen()
        options = [
            "1. Add Course Record",
            "2. Delete Course Record",
            "3. Search Course",
            "4. View All Courses",
            "5. Enroll Student in Course",
            "6. Assign Faculty to Course",
            "7. Back to Main Menu"
        ]
        utils.print_box_menu("Course Management", options)
        choice = utils.get_valid_choice("Choose option: ", ["1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "1":
            add_course(data)
            utils.pause()
        elif choice == "2":
            delete_course(data)
            utils.pause()
        elif choice == "3":
            search_courses(data)
            utils.pause()
        elif choice == "4":
            view_all_courses(data)
            utils.pause()
        elif choice == "5":
            assign_student_to_course(data)
            utils.pause()
        elif choice == "6":
            assign_faculty_to_course_wrapper(data)
            utils.pause()
        elif choice == "7":
            break
