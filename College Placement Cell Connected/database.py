import sqlite3

connection = sqlite3.connect("placement.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT,
    name TEXT,
    email TEXT,
    course TEXT,
    department TEXT,
    cgpa REAL,
    year TEXT,
    status TEXT DEFAULT 'Active'
)
""")

cursor.execute("""
INSERT INTO students (roll_no, name, email, course, department, cgpa, year, status)
VALUES ('21CS001', 'Anu', 'anu@gmail.com', 'BTech', 'CSE', 8.0, '3rd Year', 'Pending')
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    role TEXT,
    location TEXT,
    package TEXT,
    eligibility TEXT,
    skills TEXT,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE applications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_email TEXT,
    job_id INTEGER,
    company TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS recruiters(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    company TEXT,
    status TEXT DEFAULT 'Active'
)
""")

cursor.execute("""
INSERT INTO recruiters (name, email, company, status)
VALUES ('John Doe', 'john@abc.com', 'ABC Pvt Ltd', 'Active')
""")

connection.commit()

connection.close()

print("Database Created Successfully")