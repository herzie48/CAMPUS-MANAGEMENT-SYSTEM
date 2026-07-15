import utils
import file_manager
import login

def add_faculty(data):
    """Adds a new faculty member and registers a corresponding login account."""
    utils.print_header("Add Faculty Record")
    faculty = data["faculty"]
    
    fid = utils.get_valid_string("Enter Faculty ID (e.g. F1001): ").upper()
    if fid in faculty:
        utils.print_error(f"Faculty with ID {fid} already exists.")
        return
        
    name = utils.get_valid_string("Enter Faculty Name: ")
    age = utils.get_valid_int("Enter Age: ", min_val=21, max_val=75)
    gender = utils.get_valid_gender("Enter Gender (Male/Female/Other): ")
    dept = utils.get_valid_string("Enter Department: ")
    phone = utils.get_valid_phone("Enter Phone (10 digits): ")
    email = utils.get_valid_email("Enter Email: ")
    
    # Store faculty details
    faculty[fid] = {
        "faculty_id": fid,
        "name": name,
        "age": age,
        "gender": gender,
        "department": dept,
        "phone": phone,
        "email": email,
        "courses": []  # Empty assignment list initially
    }
    file_manager.save_faculty(faculty)
    
    # Create default user account: username is faculty ID, password is fac123
    login.add_user_account(fid, "fac123", "faculty", data)
    
    utils.print_success(f"Faculty member {name} added successfully! Default login created.")

def remove_faculty(data):
    """Deletes a faculty member and cascades deletion to user accounts and course teachings."""
    utils.print_header("Remove Faculty Record")
    faculty = data["faculty"]
    
    fid = utils.get_valid_string("Enter Faculty ID to delete: ").upper()
    if fid not in faculty:
        utils.print_error("Faculty member not found.")
        return
        
    confirm = input(f"Are you sure you want to remove {faculty[fid]['name']}? (Y/N): ").strip().upper()
    if confirm != 'Y':
        utils.print_info("Removal cancelled.")
        return
        
    name = faculty[fid]["name"]
    
    # Remove from courses taught by this faculty member
    courses = data["courses"]
    for code, crs in courses.items():
        if crs["faculty_id"] == fid:
            crs["faculty_id"] = ""
    file_manager.save_courses(courses)
    
    # Delete login account
    login.remove_user_account(fid, data)
    
    # Delete faculty record
    del faculty[fid]
    file_manager.save_faculty(faculty)
    
    utils.print_success(f"Faculty member {name} removed successfully.")

def update_faculty(data):
    """Allows selective editing of faculty record fields."""
    utils.print_header("Update Faculty Record")
    faculty = data["faculty"]
    
    fid = utils.get_valid_string("Enter Faculty ID to update: ").upper()
    if fid not in faculty:
        utils.print_error("Faculty member not found.")
        return
        
    fac = faculty[fid]
    print(f"Updating record for {fac['name']} ({fid}). Leave blank to keep current values.")
    
    name_input = input(f"Name [{fac['name']}]: ").strip()
    if name_input:
        fac["name"] = name_input
        
    age_input = input(f"Age [{fac['age']}]: ").strip()
    if age_input:
        try:
            age = int(age_input)
            if 21 <= age <= 75:
                fac["age"] = age
            else:
                utils.print_warning("Invalid age limits. Retained current value.")
        except ValueError:
            utils.print_warning("Invalid age input. Retained current.")
            
    gender_input = input(f"Gender [{fac['gender']}]: ").strip().capitalize()
    if gender_input:
        if gender_input in ["Male", "Female", "Other"]:
            fac["gender"] = gender_input
        else:
            utils.print_warning("Invalid gender. Retained current.")
            
    dept_input = input(f"Department [{fac['department']}]: ").strip()
    if dept_input:
        fac["department"] = dept_input
        
    phone_input = input(f"Phone [{fac['phone']}]: ").strip()
    if phone_input:
        if phone_input.isdigit() and len(phone_input) == 10:
            fac["phone"] = phone_input
        else:
            utils.print_warning("Invalid phone format. Retained current.")
            
    email_input = input(f"Email [{fac['email']}]: ").strip()
    if email_input:
        if "@" in email_input and "." in email_input:
            fac["email"] = email_input
        else:
            utils.print_warning("Invalid email format. Retained current.")
            
    file_manager.save_faculty(faculty)
    utils.print_success("Faculty record updated successfully.")

def search_faculty(data):
    """Searches faculty members by ID, name, or department."""
    utils.print_header("Search Faculty Records")
    query = utils.get_valid_string("Enter search term (ID, Name, Dept): ").lower()
    
    headers = ["Faculty ID", "Name", "Age", "Gender", "Department", "Phone", "Email", "Courses Assigned"]
    rows = []
    
    for fid, fac in data["faculty"].items():
        if (query in fid.lower() or 
            query in fac["name"].lower() or 
            query in fac["department"].lower()):
            courses_str = ", ".join(fac["courses"]) if fac["courses"] else "None"
            rows.append([fid, fac["name"], fac["age"], fac["gender"], fac["department"], fac["phone"], fac["email"], courses_str])
            
    utils.print_table(headers, rows)

def view_all_faculty(data):
    """Renders a grid of all registered faculty members."""
    utils.print_header("All Registered Faculty Members")
    headers = ["Faculty ID", "Name", "Age", "Gender", "Department", "Phone", "Email", "Courses Assigned"]
    rows = []
    
    for fid, fac in data["faculty"].items():
        courses_str = ", ".join(fac["courses"]) if fac["courses"] else "None"
        rows.append([
            fid, fac["name"], fac["age"], fac["gender"], 
            fac["department"], fac["phone"], fac["email"], courses_str
        ])
        
    utils.print_table(headers, rows)

def assign_faculty_to_course(data):
    """Assigns a faculty member to a specific course code, keeping links synced."""
    utils.print_header("Assign Faculty to Course")
    
    fid = utils.get_valid_string("Enter Faculty ID: ").upper()
    if fid not in data["faculty"]:
        utils.print_error("Faculty ID not found.")
        return
        
    code = utils.get_valid_string("Enter Course Code: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course code not found.")
        return
        
    course = data["courses"][code]
    old_faculty_id = course["faculty_id"]
    
    # Sync: If the course was assigned to another faculty member, remove it from their records
    if old_faculty_id and old_faculty_id != fid:
        if old_faculty_id in data["faculty"]:
            if code in data["faculty"][old_faculty_id]["courses"]:
                data["faculty"][old_faculty_id]["courses"].remove(code)
                
    # Update course assignment
    course["faculty_id"] = fid
    
    # Update faculty assignment list
    if code not in data["faculty"][fid]["courses"]:
        data["faculty"][fid]["courses"].append(code)
        
    # Save both changes
    file_manager.save_courses(data["courses"])
    file_manager.save_faculty(data["faculty"])
    
    utils.print_success(f"Course {code} successfully assigned to faculty {data['faculty'][fid]['name']} ({fid}).")

def faculty_management_menu(data):
    """Sub-menu dashboard for Faculty Management."""
    while True:
        utils.clear_screen()
        options = [
            "1. Add Faculty Record",
            "2. Remove Faculty Record",
            "3. Update Faculty Details",
            "4. Search Faculty Record",
            "5. View All Faculty",
            "6. Assign Faculty to Course",
            "7. Back to Main Menu"
        ]
        utils.print_box_menu("Faculty Management", options)
        choice = utils.get_valid_choice("Choose option: ", ["1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "1":
            add_faculty(data)
            utils.pause()
        elif choice == "2":
            remove_faculty(data)
            utils.pause()
        elif choice == "3":
            update_faculty(data)
            utils.pause()
        elif choice == "4":
            search_faculty(data)
            utils.pause()
        elif choice == "5":
            view_all_faculty(data)
            utils.pause()
        elif choice == "6":
            assign_faculty_to_course(data)
            utils.pause()
        elif choice == "7":
            break
