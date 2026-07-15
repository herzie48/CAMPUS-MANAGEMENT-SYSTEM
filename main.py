import sys
import utils
import file_manager
import login
import students
import faculty
import courses
import attendance
import marks
import fees
import library
import notices
import analytics
import graphs
import reports

# Professional ASCII Art Banner
ASCII_BANNER = f"""{utils.COLOR_BLUE}
  ____                                __  __                                                 _   
 / ___|__ _ _ __ ___  _ __  _   _ ___|  \\/  | __ _ _ __   __ _  __ _  ___ _ __ ___   ___ _ __ | |_ 
| |   / _` | '_ ` _ \\| '_ \\| | | / __| |\\/| |/ _` | '_ \\ / _` |/ _` |/ _ \\ '_ ` _ \\ / _ \\ '_ \\| __|
| |__| (_| | | | | | | |_) | |_| \\__ \\ |  | | (_| | | | | (_| | (_| |  __/ | | | | |  __/ | | | |_ 
 \\____\\__,_|_| |_| |_| .__/ \\__,_|___/_|  |_|\\__,_|_| |_|\\__,_|\\__, |\\___|_| |_| |_|\\___|_| |_|\\__|
                     |_|                                       |___/                              
{utils.COLOR_RESET}"""

def show_welcome_screen():
    """Displays a colorful welcome page with ASCII banner."""
    utils.clear_screen()
    print(ASCII_BANNER)
    print(f"{utils.COLOR_GREEN}{'=' * 98}")
    print(f"{'Welcome to the Campus Management System'.center(98)}")
    print(f"{'=' * 98}{utils.COLOR_RESET}\n")

def show_dashboard_header(data, username, role):
    """Prints the dashboard header containing current user information, time, and statistics."""
    utils.clear_screen()
    print(f"{utils.COLOR_CYAN}╔{'═' * 72}╗")
    print(f"║ {utils.COLOR_BOLD}CAMPUS MANAGEMENT DASHBOARD{utils.COLOR_RESET}{utils.COLOR_CYAN}".ljust(81) + "║")
    print(f"║ User: {username.ljust(15)} | Role: {role.upper().ljust(10)} | Date & Time: {utils.get_current_datetime().ljust(19)} ║")
    print(f"╠{'═' * 72}╣")
    
    # Calculate live statistics
    total_students = len(data["students"])
    total_faculty = len(data["faculty"])
    total_courses = len(data["courses"])
    total_books = sum(bk["quantity"] for bk in data["books"].values())
    
    stats_line = (f"Stats: Students: {utils.COLOR_GREEN}{total_students}{utils.COLOR_CYAN} | "
                  f"Faculty: {utils.COLOR_GREEN}{total_faculty}{utils.COLOR_CYAN} | "
                  f"Courses: {utils.COLOR_GREEN}{total_courses}{utils.COLOR_CYAN} | "
                  f"Library Books: {utils.COLOR_GREEN}{total_books}{utils.COLOR_CYAN}")
    
    # Pad string taking color code codes into account
    print(f"║ {stats_line.ljust(108)} ║")
    print(f"╚{'═' * 72}╝{utils.COLOR_RESET}\n")

def admin_menu(data, username):
    """Displays the full-featured dashboard for administrators."""
    while True:
        show_dashboard_header(data, username, "admin")
        options = [
            "1. Student Management",
            "2. Faculty Management",
            "3. Course Management",
            "4. Attendance Management",
            "5. Examination Management",
            "6. Library Management",
            "7. Fee Management",
            "8. Notice Board",
            "9. Generate Reports",
            "10. NumPy Analytics",
            "11. Matplotlib Visualizations",
            "12. Change Password",
            "13. Logout"
        ]
        utils.print_box_menu("Admin Portal Options", options)
        choice = utils.get_valid_choice("Choose option (1-13): ", [str(i) for i in range(1, 14)])
        
        if choice == "1":
            students.student_management_menu(data)
        elif choice == "2":
            faculty.faculty_management_menu(data)
        elif choice == "3":
            courses.course_management_menu(data)
        elif choice == "4":
            attendance.attendance_menu(data)
        elif choice == "5":
            marks.marks_menu(data)
        elif choice == "6":
            library.library_menu(data)
        elif choice == "7":
            fees.fees_menu(data)
        elif choice == "8":
            notices.notice_board_menu(data, "admin")
        elif choice == "9":
            reports.reports_menu(data)
        elif choice == "10":
            analytics.analytics_menu(data)
        elif choice == "11":
            graphs.graphs_menu(data)
        elif choice == "12":
            login.change_password(username, data)
            utils.pause()
        elif choice == "13":
            utils.print_success("Logging out of admin profile...")
            utils.pause()
            break

def faculty_menu(data, username):
    """Displays dashboard for teaching staff."""
    while True:
        show_dashboard_header(data, username, "faculty")
        
        # Display assigned courses
        fac_courses = []
        for ccode, crs in data["courses"].items():
            if crs["faculty_id"] == username:
                fac_courses.append(f"{ccode} - {crs['course_name']}")
                
        print(f"{utils.COLOR_BOLD}Assigned Course Loads:{utils.COLOR_RESET}")
        if fac_courses:
            for item in fac_courses:
                print(f"  ✔ {item}")
        else:
            print("  No courses currently assigned to teach.")
        print()
        
        options = [
            "1. Mark Attendance",
            "2. Edit Attendance",
            "3. Enter Exam Marks",
            "4. Edit Exam Marks",
            "5. View Class Reports",
            "6. Notice Board Panel",
            "7. Change Password",
            "8. Logout"
        ]
        utils.print_box_menu("Faculty Control Options", options)
        choice = utils.get_valid_choice("Choose option: ", [str(i) for i in range(1, 9)])
        
        if choice == "1":
            attendance.mark_attendance(data)
            utils.pause()
        elif choice == "2":
            attendance.edit_attendance(data)
            utils.pause()
        elif choice == "3":
            marks.add_marks(data)
            utils.pause()
        elif choice == "4":
            marks.edit_marks(data)
            utils.pause()
        elif choice == "5":
            # Grade list for their courses
            reports.generate_marks_report(data)
            utils.pause()
        elif choice == "6":
            notices.notice_board_menu(data, "faculty")
        elif choice == "7":
            login.change_password(username, data)
            utils.pause()
        elif choice == "8":
            utils.print_success("Logging out of faculty profile...")
            utils.pause()
            break

def student_menu(data, username):
    """Displays student specific dashboard view, where username is their Roll Number."""
    while True:
        show_dashboard_header(data, username, "student")
        
        # Verify student details exist
        if username not in data["students"]:
            utils.print_error("Your roll number profile is missing. Please contact Admin.")
            utils.pause()
            break
            
        std_profile = data["students"][username]
        print(f"Welcome back, {utils.COLOR_BOLD}{std_profile['name']}{utils.COLOR_RESET}!")
        print(f"Department: {std_profile['department']} | Semester: {std_profile['semester']}")
        print()
        
        options = [
            "1. View My Profile Details",
            "2. View Personal Report Card (Grades)",
            "3. View Course Attendance History",
            "4. Notice Board Announcements",
            "5. View Fee Dues & Billing",
            "6. Search Library Books Catalog",
            "7. Change Password",
            "8. Logout"
        ]
        utils.print_box_menu("Student Portal Options", options)
        choice = utils.get_valid_choice("Choose option: ", [str(i) for i in range(1, 9)])
        
        if choice == "1":
            utils.print_header("My Student Profile")
            for key, val in std_profile.items():
                print(f"  {key.replace('_', ' ').capitalize().ljust(15)}: {val}")
            utils.pause()
        elif choice == "2":
            marks.view_student_report_card(data)
            utils.pause()
        elif choice == "3":
            # Let the student view attendance for a chosen course
            attendance.view_student_attendance(data)
            utils.pause()
        elif choice == "4":
            notices.notice_board_menu(data, "student")
        elif choice == "5":
            utils.print_header("Personal Invoice Details")
            if username in data["fees"]:
                f_record = data["fees"][username]
                print(f"  Total Billings:  ₹{f_record['total_fees']:.2f}")
                print(f"  Fees Settled:    ₹{f_record['fees_paid']:.2f}")
                print(f"  Outstanding Dues: {utils.COLOR_RED}₹{f_record['pending_fees']:.2f}{utils.COLOR_RESET}")
            else:
                print("  No fee record found. Fees are clear.")
            utils.pause()
        elif choice == "6":
            library.search_books(data)
            utils.pause()
        elif choice == "7":
            login.change_password(username, data)
            utils.pause()
        elif choice == "8":
            utils.print_success("Logging out of student profile...")
            utils.pause()
            break

def main():
    """Main execution thread bootstrapping database loads and handling logins."""
    # Ensure data directory and files are configured, then load into memory
    data = file_manager.load_all_data()
    
    while True:
        show_welcome_screen()
        options = [
            "1. Enter System Portal (Login)",
            "2. Shut Down System (Exit)"
        ]
        utils.print_box_menu("Campus Portal Gateway", options)
        choice = utils.get_valid_choice("Select option: ", ["1", "2"])
        
        if choice == "1":
            username, role = login.login_user(data["users"])
            utils.pause()
            
            if username and role:
                if role == "admin":
                    admin_menu(data, username)
                elif role == "faculty":
                    faculty_menu(data, username)
                elif role == "student":
                    student_menu(data, username)
        elif choice == "2":
            utils.clear_screen()
            print(f"\n{utils.COLOR_GREEN}✔ System shut down safely. Goodbye!{utils.COLOR_RESET}\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
