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
    skills TEXT,
    status TEXT DEFAULT 'Active'
)
""")


cursor.execute("""
CREATE TABLE jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    role TEXT,
    location TEXT,
    package TEXT,
    eligibility TEXT,
    skills TEXT,
    description TEXT,
    posted_date TEXT,
    last_date TEXT
)
""")

cursor.execute("""
CREATE TABLE applications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_email TEXT,
    job_id INTEGER,
    company TEXT,
    status TEXT DEFAULT 'Pending'             
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

connection.commit()

connection.close()

print("Database Created Successfully")

