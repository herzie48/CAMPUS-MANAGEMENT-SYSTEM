import numpy as np
import utils

def analyze_course_marks(data):
    """Uses NumPy to compute performance statistics on a selected course's grade records."""
    utils.print_header("Course Grade Analytics")
    
    code = utils.get_valid_string("Enter Course Code to Analyze: ").upper()
    if code not in data["courses"]:
        utils.print_error("Course code not found.")
        return
        
    marks_list = []
    for (roll, c), mrk in data["marks"].items():
        if c == code:
            # Convert to percentage
            percentage = (mrk["marks_obtained"] / mrk["max_marks"]) * 100.0
            marks_list.append(percentage)
            
    if not marks_list:
        utils.print_info("No marks records exist for this course yet.")
        return
        
    # Convert list to NumPy array
    arr = np.array(marks_list)
    
    # Perform NumPy statistical calculations
    mean_val = np.mean(arr)
    median_val = np.median(arr)
    variance_val = np.var(arr)
    std_dev = np.std(arr)
    highest = np.max(arr)
    lowest = np.min(arr)
    
    # Calculate pass percentage (passing score is >= 40.0%)
    passing_count = np.sum(arr >= 40.0)
    pass_pct = (passing_count / len(arr)) * 100.0
    
    print(f"\nCourse Statistics for: {data['courses'][code]['course_name']} ({code})")
    print(f"Total Student Grades Logged: {len(arr)}")
    print(f"-----------------------------------------------")
    print(f"Highest Score:        {utils.COLOR_CYAN}{highest:.2f}%{utils.COLOR_RESET}")
    print(f"Lowest Score:         {utils.COLOR_CYAN}{lowest:.2f}%{utils.COLOR_RESET}")
    print(f"Average (Mean) Score: {utils.COLOR_CYAN}{mean_val:.2f}%{utils.COLOR_RESET}")
    print(f"Median Score:         {utils.COLOR_CYAN}{median_val:.2f}%{utils.COLOR_RESET}")
    print(f"Variance:             {utils.COLOR_CYAN}{variance_val:.2f}{utils.COLOR_RESET}")
    print(f"Standard Deviation:   {utils.COLOR_CYAN}{std_dev:.2f}{utils.COLOR_RESET}")
    print(f"Pass Percentage:      {utils.COLOR_GREEN if pass_pct >= 75.0 else utils.COLOR_RED}{pass_pct:.2f}%{utils.COLOR_RESET} (Passing grade is >= 40%)")

def analyze_student_cgpas(data):
    """Uses NumPy to compute statistical indexes on overall student CGPA profiles."""
    utils.print_header("Campus-Wide CGPA Analytics")
    
    cgpas = [std["cgpa"] for std in data["students"].values()]
    
    if not cgpas:
        utils.print_info("No students registered in the system.")
        return
        
    arr = np.array(cgpas)
    
    mean_val = np.mean(arr)
    median_val = np.median(arr)
    variance_val = np.var(arr)
    std_dev = np.std(arr)
    highest = np.max(arr)
    lowest = np.min(arr)
    
    print(f"Total Enrolled Students analyzed: {len(arr)}")
    print(f"-----------------------------------------------")
    print(f"Highest CGPA:         {utils.COLOR_CYAN}{highest:.2f}{utils.COLOR_RESET}")
    print(f"Lowest CGPA:          {utils.COLOR_CYAN}{lowest:.2f}{utils.COLOR_RESET}")
    print(f"Average CGPA:         {utils.COLOR_CYAN}{mean_val:.2f}{utils.COLOR_RESET}")
    print(f"Median CGPA:          {utils.COLOR_CYAN}{median_val:.2f}{utils.COLOR_RESET}")
    print(f"Variance:             {utils.COLOR_CYAN}{variance_val:.2f}{utils.COLOR_RESET}")
    print(f"Standard Deviation:   {utils.COLOR_CYAN}{std_dev:.2f}{utils.COLOR_RESET}")

def analyze_department_cgpas(data):
    """Groups students by department and runs NumPy analysis on regional averages."""
    utils.print_header("Department Performance Analytics")
    
    students = data["students"].values()
    if not students:
        utils.print_info("No student records available.")
        return
        
    # Group CGPAs by department
    dept_map = {}
    for std in students:
        dept = std["department"]
        if dept not in dept_map:
            dept_map[dept] = []
        dept_map[dept].append(std["cgpa"])
        
    headers = ["Department Name", "Student Count", "Highest CGPA", "Lowest CGPA", "Average CGPA"]
    rows = []
    
    for dept, cgpa_list in dept_map.items():
        arr = np.array(cgpa_list)
        rows.append([
            dept,
            len(arr),
            f"{np.max(arr):.2f}",
            f"{np.min(arr):.2f}",
            f"{np.mean(arr):.2f}"
        ])
        
    utils.print_table(headers, rows)

def analyze_semester_cgpas(data):
    """Groups students by semester and runs NumPy analysis on class-wide averages."""
    utils.print_header("Semester Performance Analytics")
    
    students = data["students"].values()
    if not students:
        utils.print_info("No student records available.")
        return
        
    # Group CGPAs by semester
    sem_map = {}
    for std in students:
        sem = std["semester"]
        if sem not in sem_map:
            sem_map[sem] = []
        sem_map[sem].append(std["cgpa"])
        
    headers = ["Semester", "Student Count", "Highest CGPA", "Lowest CGPA", "Average CGPA"]
    rows = []
    
    for sem in sorted(sem_map.keys()):
        arr = np.array(sem_map[sem])
        rows.append([
            f"Semester {sem}",
            len(arr),
            f"{np.max(arr):.2f}",
            f"{np.min(arr):.2f}",
            f"{np.mean(arr):.2f}"
        ])
        
    utils.print_table(headers, rows)

def analytics_menu(data):
    """Sub-menu interface for NumPy analytics operations."""
    while True:
        utils.clear_screen()
        options = [
            "1. Course Grade Analytics (Mean, Median, StdDev, Pass %)",
            "2. Campus CGPA Analytics (Overall Descriptive Stats)",
            "3. Department Performance Breakdown (Average CGPA)",
            "4. Semester Performance Breakdown (Average CGPA)",
            "5. Back to Main Menu"
        ]
        utils.print_box_menu("NumPy Analytics Dashboard", options)
        choice = utils.get_valid_choice("Choose option: ", ["1", "2", "3", "4", "5"])
        
        if choice == "1":
            analyze_course_marks(data)
            utils.pause()
        elif choice == "2":
            analyze_student_cgpas(data)
            utils.pause()
        elif choice == "3":
            analyze_department_cgpas(data)
            utils.pause()
        elif choice == "4":
            analyze_semester_cgpas(data)
            utils.pause()
        elif choice == "5":
            break
