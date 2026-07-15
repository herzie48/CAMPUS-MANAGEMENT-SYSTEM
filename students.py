import utils
import file_manager
import login

def add_student(data):
    """Adds a new student to the system and creates associated fees and user accounts."""
    utils.print_header("Add Student Record")
    students = data["students"]
    
    roll = utils.get_valid_roll_number("Enter Roll Number (e.g. CS1001): ")
    if roll in students:
        utils.print_error(f"Student with Roll Number {roll} already exists.")
        return
        
    name = utils.get_valid_string("Enter Student Name: ")
    age = utils.get_valid_int("Enter Age: ", min_val=15, max_val=60)
    gender = utils.get_valid_gender("Enter Gender (Male/Female/Other): ")
    dept = utils.get_valid_string("Enter Department (e.g. Computer Science): ")
    sem = utils.get_valid_int("Enter Semester (1-8): ", min_val=1, max_val=8)
    phone = utils.get_valid_phone("Enter Phone (10 digits): ")
    email = utils.get_valid_email("Enter Email: ")
    address = utils.get_valid_string("Enter Address: ")
    cgpa = utils.get_valid_float("Enter CGPA (0.0 - 10.0): ", min_val=0.0, max_val=10.0)
    
    # Store student details
    students[roll] = {
        "roll_number": roll,
        "name": name,
        "age": age,
        "gender": gender,
        "department": dept,
        "semester": sem,
        "phone": phone,
        "email": email,
        "address": address,
        "cgpa": cgpa
    }
    file_manager.save_students(students)
    
    # Create default user account: username is roll number, password is std123
    login.add_user_account(roll, "std123", "student", data)
    
    # Initialize default fees record: 50,000 total, 0 paid, 50,000 pending
    data["fees"][roll] = {
        "roll_number": roll,
        "total_fees": 50000.0,
        "fees_paid": 0.0,
        "pending_fees": 50000.0
    }
    file_manager.save_fees(data["fees"])
    
    utils.print_success(f"Student {name} added successfully! Default login created.")

def update_student(data):
    """Allows selective updating of a student's attributes by roll number."""
    utils.print_header("Update Student Record")
    students = data["students"]
    
    roll = utils.get_valid_roll_number("Enter Roll Number to update: ")
    if roll not in students:
        utils.print_error("Student not found.")
        return
        
    std = students[roll]
    print(f"Updating record for {std['name']} ({roll}). Leave blank and press Enter to keep current values.")
    
    # Update fields optionally
    name_input = input(f"Name [{std['name']}]: ").strip()
    if name_input:
        std["name"] = name_input
        
    age_input = input(f"Age [{std['age']}]: ").strip()
    if age_input:
        try:
            age = int(age_input)
            if 15 <= age <= 60:
                std["age"] = age
            else:
                utils.print_warning("Invalid age bounds. Retained current value.")
        except ValueError:
            utils.print_warning("Invalid age input. Retained current value.")
            
    gender_input = input(f"Gender [{std['gender']}]: ").strip().capitalize()
    if gender_input:
        if gender_input in ["Male", "Female", "Other"]:
            std["gender"] = gender_input
        else:
            utils.print_warning("Invalid gender. Retained current value.")
            
    dept_input = input(f"Department [{std['department']}]: ").strip()
    if dept_input:
        std["department"] = dept_input
        
    sem_input = input(f"Semester [{std['semester']}]: ").strip()
    if sem_input:
        try:
            sem = int(sem_input)
            if 1 <= sem <= 8:
                std["semester"] = sem
            else:
                utils.print_warning("Semester must be between 1 and 8. Retained current value.")
        except ValueError:
            utils.print_warning("Invalid semester input. Retained current value.")
            
    phone_input = input(f"Phone [{std['phone']}]: ").strip()
    if phone_input:
        if phone_input.isdigit() and len(phone_input) == 10:
            std["phone"] = phone_input
        else:
            utils.print_warning("Invalid phone format. Retained current value.")
            
    email_input = input(f"Email [{std['email']}]: ").strip()
    if email_input:
        if "@" in email_input and "." in email_input:
            std["email"] = email_input
        else:
            utils.print_warning("Invalid email. Retained current value.")
            
    addr_input = input(f"Address [{std['address']}]: ").strip()
    if addr_input:
        std["address"] = addr_input
        
    cgpa_input = input(f"CGPA [{std['cgpa']}]: ").strip()
    if cgpa_input:
        try:
            cgpa = float(cgpa_input)
            if 0.0 <= cgpa <= 10.0:
                std["cgpa"] = cgpa
            else:
                utils.print_warning("CGPA must be between 0.0 and 10.0. Retained current value.")
        except ValueError:
            utils.print_warning("Invalid CGPA input. Retained current value.")
            
    file_manager.save_students(students)
    utils.print_success("Student record updated successfully.")

def delete_student(data):
    """Deletes a student and cascades deletion to user accounts, courses, marks, fees, and library books."""
    utils.print_header("Delete Student Record")
    students = data["students"]
    
    roll = utils.get_valid_roll_number("Enter Roll Number to delete: ")
    if roll not in students:
        utils.print_error("Student not found.")
        return
        
    confirm = input(f"Are you sure you want to delete {students[roll]['name']}? (Y/N): ").strip().upper()
    if confirm != 'Y':
        utils.print_info("Deletion cancelled.")
        return
        
    name = students[roll]["name"]
    
    # 1. Delete student record
    del students[roll]
    file_manager.save_students(students)
    
    # 2. Delete login account
    login.remove_user_account(roll, data)
    
    # 3. Delete fees record
    if roll in data["fees"]:
        del data["fees"][roll]
        file_manager.save_fees(data["fees"])
        
    # 4. Remove student from courses enrollment
    courses = data["courses"]
    for code, crs in courses.items():
        if roll in crs["students"]:
            crs["students"].remove(roll)
    file_manager.save_courses(courses)
    
    # 5. Delete student's marks records
    marks = data["marks"]
    keys_to_delete = [k for k in marks.keys() if k[0] == roll]
    for k in keys_to_delete:
        del marks[k]
    file_manager.save_marks(marks)
    
    # 6. Delete student's attendance records
    attendance = data["attendance"]
    att_keys_to_delete = [k for k in attendance.keys() if k[0] == roll]
    for k in att_keys_to_delete:
        del attendance[k]
    file_manager.save_attendance(attendance)
    
    # 7. Return borrowed books if any
    books = data["books"]
    for bid, bk in books.items():
        if roll in bk["borrowed_by"]:
            del bk["borrowed_by"][roll]
    file_manager.save_books(books)
            
    utils.print_success(f"Student {name} and all related records deleted.")

def search_students(data):
    """Searches student records matching roll number, name, department, or semester."""
    utils.print_header("Search Student Records")
    query = utils.get_valid_string("Enter search term (Roll No, Name, Dept, Sem): ").lower()
    
    headers = ["Roll No", "Name", "Age", "Gender", "Department", "Sem", "CGPA"]
    rows = []
    
    for roll, std in data["students"].items():
        if (query in roll.lower() or 
            query in std["name"].lower() or 
            query in std["department"].lower() or 
            query == str(std["semester"])):
            rows.append([roll, std["name"], std["age"], std["gender"], std["department"], std["semester"], std["cgpa"]])
            
    utils.print_table(headers, rows)

def view_all_students(data):
    """Displays all student records."""
    utils.print_header("All Registered Students")
    headers = ["Roll No", "Name", "Age", "Gender", "Department", "Sem", "CGPA", "Phone", "Email"]
    rows = []
    
    for roll, std in data["students"].items():
        rows.append([
            roll, std["name"], std["age"], std["gender"], 
            std["department"], std["semester"], std["cgpa"], 
            std["phone"], std["email"]
        ])
        
    utils.print_table(headers, rows)

def sort_students_menu(data):
    """Sorts student lists and prints them in tabular layout."""
    utils.print_header("Sort Student Records")
    options = [
        "1. Sort by Name",
        "2. Sort by Roll Number",
        "3. Sort by CGPA (Highest First)",
        "4. Back"
    ]
    utils.print_box_menu("Sorting Options", options)
    choice = utils.get_valid_choice("Enter choice: ", ["1", "2", "3", "4"])
    
    if choice == "4":
        return
        
    std_list = list(data["students"].values())
    if not std_list:
        utils.print_info("No students registered yet.")
        return
        
    if choice == "1":
        sorted_list = sorted(std_list, key=lambda x: x["name"].lower())
        title = "Students Sorted by Name"
    elif choice == "2":
        sorted_list = sorted(std_list, key=lambda x: x["roll_number"])
        title = "Students Sorted by Roll Number"
    elif choice == "3":
        sorted_list = sorted(std_list, key=lambda x: x["cgpa"], reverse=True)
        title = "Students Sorted by CGPA (Desc)"
        
    utils.print_header(title)
    headers = ["Roll No", "Name", "Department", "Semester", "CGPA"]
    rows = [[s["roll_number"], s["name"], s["department"], s["semester"], s["cgpa"]] for s in sorted_list]
    utils.print_table(headers, rows)

def student_management_menu(data):
    """Nested menu interface for Student Management."""
    while True:
        utils.clear_screen()
        options = [
            "1. Add Student",
            "2. Update Student",
            "3. Delete Student",
            "4. Search Student",
            "5. View All Students",
            "6. Sort Students",
            "7. Back to Main Menu"
        ]
        utils.print_box_menu("Student Management", options)
        choice = utils.get_valid_choice("Choose option: ", ["1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "1":
            add_student(data)
            utils.pause()
        elif choice == "2":
            update_student(data)
            utils.pause()
        elif choice == "3":
            delete_student(data)
            utils.pause()
        elif choice == "4":
            search_students(data)
            utils.pause()
        elif choice == "5":
            view_all_students(data)
            utils.pause()
        elif choice == "6":
            sort_students_menu(data)
            utils.pause()
        elif choice == "7":
            break
