import os

# Define relative paths to data files
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.txt")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
FACULTY_FILE = os.path.join(DATA_DIR, "faculty.txt")
COURSES_FILE = os.path.join(DATA_DIR, "courses.txt")
ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.txt")
MARKS_FILE = os.path.join(DATA_DIR, "marks.txt")
FEES_FILE = os.path.join(DATA_DIR, "fees.txt")
BOOKS_FILE = os.path.join(DATA_DIR, "books.txt")
NOTICES_FILE = os.path.join(DATA_DIR, "notices.txt")

def ensure_data_files_exist():
    """Checks if the data directory and all text files exist.
    If not, creates them and seeds users.txt with default accounts.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    files = [
        USERS_FILE, STUDENTS_FILE, FACULTY_FILE, COURSES_FILE,
        ATTENDANCE_FILE, MARKS_FILE, FEES_FILE, BOOKS_FILE, NOTICES_FILE
    ]
    
    for file_path in files:
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                pass  # Create empty file
                
    # Seed default users if users.txt is empty
    if os.path.getsize(USERS_FILE) == 0:
        with open(USERS_FILE, "w") as f:
            f.write("admin|admin123|admin\n")
            f.write("faculty|faculty123|faculty\n")
            f.write("student|student123|student\n")

def load_users():
    """Loads users from users.txt into a dictionary."""
    users = {}
    if not os.path.exists(USERS_FILE):
        return users
    with open(USERS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 3:
                username, password, role = parts
                users[username] = {"username": username, "password": password, "role": role}
    return users

def save_users(users):
    """Saves users dictionary back to users.txt."""
    with open(USERS_FILE, "w") as f:
        for username, user_data in users.items():
            f.write(f"{user_data['username']}|{user_data['password']}|{user_data['role']}\n")

def load_students():
    """Loads students from students.txt."""
    students = {}
    if not os.path.exists(STUDENTS_FILE):
        return students
    with open(STUDENTS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 10:
                roll, name, age, gender, dept, sem, phone, email, addr, cgpa = parts
                students[roll] = {
                    "roll_number": roll,
                    "name": name,
                    "age": int(age),
                    "gender": gender,
                    "department": dept,
                    "semester": int(sem),
                    "phone": phone,
                    "email": email,
                    "address": addr,
                    "cgpa": float(cgpa)
                }
    return students

def save_students(students):
    """Saves students dictionary to students.txt."""
    with open(STUDENTS_FILE, "w") as f:
        for roll, std in students.items():
            f.write(f"{std['roll_number']}|{std['name']}|{std['age']}|{std['gender']}|"
                    f"{std['department']}|{std['semester']}|{std['phone']}|{std['email']}|"
                    f"{std['address']}|{std['cgpa']}\n")

def load_faculty():
    """Loads faculty from faculty.txt."""
    faculty = {}
    if not os.path.exists(FACULTY_FILE):
        return faculty
    with open(FACULTY_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 8:
                fid, name, age, gender, dept, phone, email, courses_assigned_str = parts
                courses = []
                if courses_assigned_str and courses_assigned_str != "None":
                    courses = courses_assigned_str.split(",")
                faculty[fid] = {
                    "faculty_id": fid,
                    "name": name,
                    "age": int(age),
                    "gender": gender,
                    "department": dept,
                    "phone": phone,
                    "email": email,
                    "courses": courses
                }
    return faculty

def save_faculty(faculty):
    """Saves faculty dictionary to faculty.txt."""
    with open(FACULTY_FILE, "w") as f:
        for fid, fac in faculty.items():
            courses_str = ",".join(fac["courses"]) if fac["courses"] else "None"
            f.write(f"{fac['faculty_id']}|{fac['name']}|{fac['age']}|{fac['gender']}|"
                    f"{fac['department']}|{fac['phone']}|{fac['email']}|{courses_str}\n")

def load_courses():
    """Loads courses from courses.txt."""
    courses = {}
    if not os.path.exists(COURSES_FILE):
        return courses
    with open(COURSES_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 6:
                code, name, dept, credits, fid, students_str = parts
                faculty_id = "" if fid == "None" or not fid else fid
                student_rolls = []
                if students_str and students_str != "None":
                    student_rolls = students_str.split(",")
                courses[code] = {
                    "course_code": code,
                    "course_name": name,
                    "department": dept,
                    "credits": int(credits),
                    "faculty_id": faculty_id,
                    "students": student_rolls
                }
    return courses

def save_courses(courses):
    """Saves courses dictionary to courses.txt."""
    with open(COURSES_FILE, "w") as f:
        for code, crs in courses.items():
            fid = crs["faculty_id"] if crs["faculty_id"] else "None"
            students_str = ",".join(crs["students"]) if crs["students"] else "None"
            f.write(f"{crs['course_code']}|{crs['course_name']}|{crs['department']}|"
                    f"{crs['credits']}|{fid}|{students_str}\n")

def load_attendance():
    """Loads attendance from attendance.txt into a dictionary keyed by (roll_number, course_code, date)."""
    attendance = {}
    if not os.path.exists(ATTENDANCE_FILE):
        return attendance
    with open(ATTENDANCE_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 4:
                roll, code, date, status = parts
                attendance[(roll, code, date)] = status
    return attendance

def save_attendance(attendance):
    """Saves attendance dictionary to attendance.txt."""
    with open(ATTENDANCE_FILE, "w") as f:
        for (roll, code, date), status in attendance.items():
            f.write(f"{roll}|{code}|{date}|{status}\n")

def load_marks():
    """Loads marks from marks.txt into a dictionary keyed by (roll_number, course_code)."""
    marks = {}
    if not os.path.exists(MARKS_FILE):
        return marks
    with open(MARKS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 4:
                roll, code, obtained, max_m = parts
                marks[(roll, code)] = {
                    "roll_number": roll,
                    "course_code": code,
                    "marks_obtained": float(obtained),
                    "max_marks": float(max_m)
                }
    return marks

def save_marks(marks):
    """Saves marks dictionary to marks.txt."""
    with open(MARKS_FILE, "w") as f:
        for (roll, code), mrk in marks.items():
            f.write(f"{roll}|{code}|{mrk['marks_obtained']}|{mrk['max_marks']}\n")

def load_fees():
    """Loads fees from fees.txt into a dictionary keyed by roll_number."""
    fees = {}
    if not os.path.exists(FEES_FILE):
        return fees
    with open(FEES_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 4:
                roll, total, paid, pending = parts
                fees[roll] = {
                    "roll_number": roll,
                    "total_fees": float(total),
                    "fees_paid": float(paid),
                    "pending_fees": float(pending)
                }
    return fees

def save_fees(fees):
    """Saves fees dictionary to fees.txt."""
    with open(FEES_FILE, "w") as f:
        for roll, fee in fees.items():
            f.write(f"{roll}|{fee['total_fees']}|{fee['fees_paid']}|{fee['pending_fees']}\n")

def load_books():
    """Loads books from books.txt."""
    books = {}
    if not os.path.exists(BOOKS_FILE):
        return books
    with open(BOOKS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 5:
                bid, title, author, qty, borrowed_str = parts
                borrowed_dict = {}
                if borrowed_str and borrowed_str != "None":
                    pairs = borrowed_str.split(",")
                    for pair in pairs:
                        if ":" in pair:
                            roll, due_date = pair.split(":")
                            borrowed_dict[roll] = due_date
                books[bid] = {
                    "book_id": bid,
                    "title": title,
                    "author": author,
                    "quantity": int(qty),
                    "borrowed_by": borrowed_dict
                }
    return books

def save_books(books):
    """Saves books dictionary to books.txt."""
    with open(BOOKS_FILE, "w") as f:
        for bid, bk in books.items():
            borrowed_str = "None"
            if bk["borrowed_by"]:
                borrowed_str = ",".join([f"{roll}:{due}" for roll, due in bk["borrowed_by"].items()])
            f.write(f"{bk['book_id']}|{bk['title']}|{bk['author']}|{bk['quantity']}|{borrowed_str}\n")

def load_notices():
    """Loads notices from notices.txt."""
    notices = {}
    if not os.path.exists(NOTICES_FILE):
        return notices
    with open(NOTICES_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) == 4:
                nid, date, title, content = parts
                notices[nid] = {
                    "notice_id": nid,
                    "date": date,
                    "title": title,
                    "content": content
                }
    return notices

def save_notices(notices):
    """Saves notices dictionary to notices.txt."""
    with open(NOTICES_FILE, "w") as f:
        for nid, note in notices.items():
            f.write(f"{note['notice_id']}|{note['date']}|{note['title']}|{note['content']}\n")

def load_all_data():
    """Helper to initialize file system and load all datasets into a single nested dictionary."""
    ensure_data_files_exist()
    return {
        "users": load_users(),
        "students": load_students(),
        "faculty": load_faculty(),
        "courses": load_courses(),
        "attendance": load_attendance(),
        "marks": load_marks(),
        "fees": load_fees(),
        "books": load_books(),
        "notices": load_notices()
    }
