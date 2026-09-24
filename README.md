# Campus Management System

A complete, professional, menu-driven Campus Management System built entirely in Python. The system provides a command-line interface (CLI) styled with ANSI color codes and Unicode double-box drawings. It leverages **NumPy** for academic performance analytics and **Matplotlib** for administrative visualizations, while managing database operations through flat text files.

---

## Folder Structure

```text
Campus_Management_System/
├── data/
│   ├── attendance.txt   # Attendance logs (roll_number|course_code|date|status)
│   ├── books.txt        # Library books catalog & borrows
│   ├── courses.txt      # Course records & student enrollments
│   ├── faculty.txt      # Faculty details & course assignments
│   ├── fees.txt         # Financial billings & payments
│   ├── marks.txt        # Student grades for enrolled courses
│   ├── notices.txt      # Campus announcement board
│   ├── students.txt     # Student demographic details
│   └── users.txt        # Authentication logins (username|password|role)
├── analytics.py        # Descriptive statistics engine using NumPy
├── attendance.py       # Attendance tracking, percentages, and alerts
├── courses.py          # Course catalog entries & enrollments
├── faculty.py          # Faculty profiles & course mappings
├── fees.py             # Billing invoices, transaction payments, receipts
├── file_manager.py     # Database serializer/parser for text files
├── graphs.py           # Matplotlib visualization plotter
├── library.py          # Book borrows, return cycles, and overdue fines
├── login.py            # Authentication, password change, and validation
├── main.py             # Entrypoint displaying user portals & live stats
├── marks.py            # Grades management, toppers, and GPAs
├── notices.py          # notice board publishers & displays
├── reports.py          # Demographic, financial, and class audits
└── utils.py            # Terminal console UI layout & inputs validation
```

---

## Features

### 🔐 1. Role-Based Login & Security
- Secure access split into **Admin**, **Faculty**, and **Student** portals.
- Password complexity validation.
- User management panel for resetting and changing passwords.

### 🎓 2. Student Management
- Full demographic record handling (Roll Number, Name, Age, Gender, Department, Semester, Phone, Email, Address, CGPA).
- Student searching by name, roll number, department, or semester.
- Sorting systems (arrange by name, roll number, or CGPA descending).

### 👔 3. Faculty Management
- Add, update, and search faculty profiles.
- Course assignments matching faculty teaching loads.

### 📚 4. Course Enrollment
- Manage course credits, departments, and course-specific details.
- Enroll students and assign course-teachers keeping links synchronized.

### 📅 5. Attendance Ledger
- Daily attendance marking (P/A) student-by-student per course.
- Edit attendance entries retroactively.
- Percentage calculator and monthly aggregates.
- Warning flags showing students below the standard **75%** threshold.

### 📝 6. Examination & Grading
- Enter, edit, or delete grades.
- Grade Mapping based on score percentages (O, A+, A, B+, B, C, F).
- GPA calculations (semester-GPA) and subject topper listings.
- Generate overall campus rank lists.

### 📖 7. Library System
- Catalog book copies and active borrowed statuses.
- Book checkout (limits duplicate checks of the same title, sets standard 14-day return cycles).
- Overdue return tracker charging an automated late fee of **₹10 per day** overdue (charged directly to the student's pending fees account).

### 💰 8. Fee Billing & Payments
- Tracks billing, total fees, payments, and outstanding balances.
- Print official payment receipts.
- Outstanding collection reminders showing student contacts.

### 📢 9. Announcement Notice Board
- Date-stamped announcement publisher for admin and faculty.
- Formatted bulletin boards visible to all roles.

### 📊 10. NumPy Statistics
- Calculates Course average scores, means, medians, variances, and standard deviations.
- Evaluates department-wide and semester-wide performance markers.

### 📈 11. Visualizations (Matplotlib)
- **Line Graph**: Course daily attendance trends.
- **Histogram**: Mark score spreads.
- **Bar Charts**: Average CGPA per department, active library borrows per book title.
- **Pie Charts**: Grade distributions, overall paid vs pending fee collections.

---

## Required Libraries

Ensure Python (3.8+) is installed on your system. Install required external libraries:

```bash
pip install numpy matplotlib
```

---

## Installation & How to Run

1. Clone or download the `Campus_Management_System` folder directory onto your system.
2. Open a terminal/command prompt and navigate into the folder:
   ```bash
   cd Campus_Management_System
   ```
3. Run the system entrypoint script:
   ```bash
   python main.py
   ```

---

## Default Login Credentials

Upon first launch, the program automatically boots up the `data/` files and seeds default login credentials:

| Portal Role | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` |
| **Faculty** | `faculty` | `faculty123` |
| **Student** | `student` | `student123` |

---


## Future Improvements

- Implement encryption hash algorithms (like `hashlib`) for password records in `users.txt`.
- Add CSV export utilities for administrative report spreadsheets.
- Add course prerequisite checks during student enrollments.
