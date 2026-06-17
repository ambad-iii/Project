import sqlite3

connection = sqlite3.connect("placement.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    course TEXT,
    year TEXT
)
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

connection.commit()

connection.close()

print("Database Created Successfully")