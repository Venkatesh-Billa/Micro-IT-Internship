import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("student_system.db")
cursor = conn.cursor()

# Create necessary tables
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT UNIQUE NOT NULL,
    class TEXT NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
    student_id INTEGER,
    date TEXT,
    status TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS grades (
    student_id INTEGER,
    subject TEXT,
    grade TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)''')

conn.commit()

# Functions

def add_student():
    name = input("Enter name: ")
    roll = input("Enter roll number: ")
    class_name = input("Enter class: ")
    try:
        cursor.execute("INSERT INTO students (name, roll_no, class) VALUES (?, ?, ?)", (name, roll, class_name))
        conn.commit()
        print("✅ Student added successfully!\n")
    except sqlite3.IntegrityError:
        print("⚠️ Student with this roll number already exists.\n")

def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    print("\n-- 🧑‍🎓 Student List --")
    for s in students:
        print(f"ID: {s[0]}, Name: {s[1]}, Roll No: {s[2]}, Class: {s[3]}")
    print()

def mark_attendance():
    roll = input("Enter student roll number: ")
    date = input("Enter date (YYYY-MM-DD): ")
    status = input("Enter status (Present/Absent): ")
    cursor.execute("SELECT id FROM students WHERE roll_no = ?", (roll,))
    student = cursor.fetchone()
    if student:
        cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                       (student[0], date, status))
        conn.commit()
        print("✅ Attendance marked.\n")
    else:
        print("⚠️ Student not found.\n")

def enter_grades():
    roll = input("Enter student roll number: ")
    subject = input("Enter subject: ")
    grade = input("Enter grade: ")
    cursor.execute("SELECT id FROM students WHERE roll_no = ?", (roll,))
    student = cursor.fetchone()
    if student:
        cursor.execute("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)",
                       (student[0], subject, grade))
        conn.commit()
        print("✅ Grade recorded.\n")
    else:
        print("⚠️ Student not found.\n")

def view_attendance():
    roll = input("Enter student roll number: ")
    cursor.execute("SELECT id FROM students WHERE roll_no = ?", (roll,))
    student = cursor.fetchone()
    if student:
        cursor.execute("SELECT date, status FROM attendance WHERE student_id = ?", (student[0],))
        records = cursor.fetchall()
        print(f"\n-- 📅 Attendance for Roll No {roll} --")
        for date, status in records:
            print(f"{date}: {status}")
        print()
    else:
        print("⚠️ Student not found.\n")

def view_grades():
    roll = input("Enter student roll number: ")
    cursor.execute("SELECT id FROM students WHERE roll_no = ?", (roll,))
    student = cursor.fetchone()
    if student:
        cursor.execute("SELECT subject, grade FROM grades WHERE student_id = ?", (student[0],))
        records = cursor.fetchall()
        print(f"\n-- 📝 Grades for Roll No {roll} --")
        for subject, grade in records:
            print(f"{subject}: {grade}")
        print()
    else:
        print("⚠️ Student not found.\n")

def delete_student():
    roll = input("Enter roll number of student to delete: ")
    cursor.execute("SELECT id FROM students WHERE roll_no = ?", (roll,))
    student = cursor.fetchone()
    if student:
        confirm = input(f"Are you sure you want to delete student with Roll No {roll}? (yes/no): ")
        if confirm.lower() == "yes":
            student_id = student[0]
            cursor.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM grades WHERE student_id = ?", (student_id,))
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
            print("✅ Student and related data deleted.\n")
        else:
            print("❌ Deletion cancelled.\n")
    else:
        print("⚠️ Student not found.\n")

# Menu

def menu():
    while True:
        print("==== 📘 Student Management System ====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Mark Attendance")
        print("4. Enter Grades")
        print("5. Exit")
        print("6. View Attendance")
        print("7. View Grades")
        print("8. Delete Student")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            mark_attendance()
        elif choice == "4":
            enter_grades()
        elif choice == "5":
            print("👋 Exiting...")
            break
        elif choice == "6":
            view_attendance()
        elif choice == "7":
            view_grades()
        elif choice == "8":
            delete_student()
        else:
            print("⚠️ Invalid choice. Try again.\n")

# Start the program
menu()
conn.close()
