from flask import Flask, render_template, request, redirect, session
import os
import sqlite3

def get_db_connection():
    conn = sqlite3.connect("placement.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT,
        company TEXT
    )
    """)
    conn.execute(
        "INSERT OR IGNORE INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
        ("Admin", "admin", "admin123", "Admin")
    )
    conn.commit()
    conn.close()

app=Flask(__name__)
app.secret_key = "mysecretkey"

UPLOAD_FOLDER='uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

init_db()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/templates/<path:filename>')
def templates_route(filename):
    if not filename.endswith('.html'):
        return redirect('/')
    return render_template(filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method=='POST':
        role=request.form.get('role')
        login_name=request.form.get('login_name')
        email=request.form.get('login_email')
        password=request.form.get('login_password')

        if role == 'Admin':
            if not role or not email or not password:
                error = "Please fill all login fields"
            else:
                conn = get_db_connection()
                user = conn.execute(
                    "SELECT * FROM users WHERE email=? AND password=? AND role=?",
                    (email, password, 'Admin')
                ).fetchone()
                conn.close()

                if user:
                    session['user'] = email
                    return redirect('/admin_dashboard')
                else:
                    error = "Invalid admin credentials"
        else:
            if not role or not login_name or not email or not password:
                error = "Please fill all login fields"
            else:
                conn = get_db_connection()
                user = conn.execute(
                    "SELECT * FROM users WHERE email=? AND password=? AND role=?",
                    (email, password, role)
                ).fetchone()
                conn.close()

                if user and user['name'] == login_name:
                    session['user'] = email
                    if role == "Student":
                        return redirect('/std_dashboard')
                    elif role == "Recruiter":
                        return redirect('/dashboard')
                else:
                    error = "Invalid login details"
    return render_template("login.html", error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        role = request.form.get('role')
        name = request.form.get('register_name')
        email = request.form.get('register_email')
        password = request.form.get('register_password')
        confirm = request.form.get('confirm')

        if not role or not name or not email or not password or not confirm:
            error = "Please fill all fields"
        elif password != confirm:
            error = "Passwords do not match"
        else:
            conn = get_db_connection()
            try:
                conn.execute(
                    "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                    (name, email, password, role)
                )
                if role == "Student":
                    conn.execute(
                        "INSERT OR IGNORE INTO students (name, email) VALUES (?, ?)",
                        (name, email)
                    )
                elif role == "Recruiter":
                    conn.execute(
                        "INSERT OR IGNORE INTO recruiters (name, email) VALUES (?, ?)",
                        (name, email)
                    )
                conn.commit()
                session['user'] = email
                if role == "Student":
                    return redirect('/std_dashboard')
                elif role == "Recruiter":
                    return redirect('/dashboard')
                elif role == "Admin":
                    return redirect('/admin_dashboard')
            except sqlite3.IntegrityError:
                error = "This email is already registered"
            finally:
                conn.close()
    return render_template('register.html', error=error)

@app.route('/std_dashboard')
def dashboard():

    conn = get_db_connection()

    jobs = conn.execute("SELECT * FROM jobs").fetchall()

    student = conn.execute("SELECT * FROM students WHERE email=?",(session.get('user'),)).fetchone()

    applications_rows = conn.execute("SELECT * FROM applications WHERE student_email=?",(session.get('user'),)).fetchall()

    conn.close()
    # convert to simple list of company names
    applied_jobs = [a["job_id"] for a in applications_rows]
    return render_template("std_dashboard.html",jobs=jobs,student=student,applications=applied_jobs)

@app.route('/std_profile')
def profile():

    conn = get_db_connection()

    student = conn.execute("SELECT * FROM students WHERE email=?",(session.get('user'),)).fetchone()

    applications = conn.execute("SELECT * FROM applications WHERE student_email=?",(session.get('user'),)).fetchall()

    conn.close()

    return render_template("std_profile.html",applications=applications,student=student)

@app.route('/std_jobs')
def jobs_page():

    conn = get_db_connection()

    student = conn.execute("SELECT * FROM students WHERE email=?",(session.get('user'),)).fetchone()

    jobs = conn.execute("SELECT * FROM jobs").fetchall()

    applications_rows = conn.execute("SELECT job_id FROM applications WHERE student_email=?",(session.get('user'),)).fetchall()

    conn.close()

    applied_jobs = [a["job_id"] for a in applications_rows]
    return render_template(
        "std_jobs.html",
        jobs=jobs,
        student=student,
        applications=applied_jobs
    )

@app.route('/std_job-details/<int:job_id>')
def job_details(job_id):

    conn = get_db_connection()
    student = conn.execute(
    "SELECT * FROM students WHERE email=?",
    (session.get('user'),)).fetchone()

    job = conn.execute("SELECT * FROM jobs WHERE id=?",(job_id,)).fetchone()

    applications_rows = conn.execute("SELECT job_id FROM applications WHERE student_email=?",(session.get('user'),)).fetchall()

    applied_jobs = [a["job_id"] for a in applications_rows]

    conn.close()   

    return render_template("std_job-details.html",job=job,student=student,applications=applied_jobs)

@app.route('/update-profile', methods=['POST'])
def update_profile():
    if request.form['name']:
        student["name"]=request.form['name']
    if request.form['email']:
        student["email"]=request.form['email']
    if request.form['course']:
        student["course"]=request.form['course']
    if request.form['year']:
        student["year"]=request.form['year']
    return redirect('/std_profile')

@app.route('/apply/<int:job_id>', methods=['POST'])
def apply_job(job_id):

    email = session.get('user')
    if not email:
        return redirect('/login')

    conn = get_db_connection()

    job = conn.execute(
    "SELECT * FROM jobs WHERE id=?",(job_id,)).fetchone()

    existing = conn.execute("""
        SELECT * FROM applications
        WHERE student_email=? AND job_id=?
    """, (email, job_id)).fetchone()

    if existing:
        conn.close()
        return redirect('/std_profile')

    conn.execute("""
        INSERT INTO applications (student_email, job_id, company)VALUES (?, ?, ?)
    """, (email, job_id, job["company"]))

    conn.commit()
    conn.close()

    return redirect('/std_profile')

@app.route('/remove-application/<int:id>', methods=['POST'])
def remove_application(id):

    email = session.get('user')

    conn = get_db_connection()

    conn.execute("""
    DELETE FROM applications WHERE id=? AND student_email=?
    """, (id, email))

    conn.commit()
    conn.close()

    return redirect('/std_profile#applications')

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    global resume_filename
    file=request.files['resume']
    if file and file.filename:
        resume_filename=file.filename 
        file.save(
            os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect('/std_profile')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/dashboard')
def recruiter_dashboard():

    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    jobs = conn.execute("SELECT * FROM jobs").fetchall()
    applications = conn.execute("SELECT * FROM applications").fetchall()

    conn.close()

    return render_template("dashboard.html",jobs=jobs,applications=applications,students=students)

# RECRUITER PROFILE
@app.route('/profile')
def recruiter_profile():
    return render_template("profile.html")


# POST JOB
@app.route('/post_job', methods=['GET', 'POST'])
def post_job():

    if request.method == 'POST':

        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        salary = request.form['salary']
        location = request.form['location']
        eligibility = request.form['elgibility']
        skills = request.form['skills']

        connection = sqlite3.connect("placement.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO jobs(company, role, location, package, eligibility, skills, description) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            company,
            title,
            location,
            salary,
            eligibility,
            skills,
            description
        ))

        connection.commit()
        connection.close()

        return redirect('/dashboard')

    return render_template("post_job.html")

# APPLICANTS
@app.route('/applicants')
def applicants():

    conn = get_db_connection()

    applications = conn.execute("""
        SELECT 
            applications.id,
            applications.student_email,
            applications.job_id,
            jobs.company,
            jobs.role
        FROM applications
        JOIN jobs ON applications.job_id = jobs.id
    """).fetchall()

    conn.close()

    return render_template("applicants.html", applicants=applications)

@app.route('/admin_dashboard')
def admin_dashboard():

    conn = get_db_connection()

    recruiters=conn.execute("SELECT * FROM recruiters").fetchall()
    students = conn.execute("SELECT * FROM students").fetchall()
    jobs = conn.execute("SELECT * FROM jobs").fetchall()
    applications = conn.execute("SELECT * FROM applications").fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        students=students,
        recruiters=recruiters,
        jobs=jobs,
        applications=applications
    )

@app.route('/admin_students')
def admin_students():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("admin_students.html", students=students)

@app.route('/admin_recruiters')
def recruiters():
    conn = get_db_connection()

    recruiters = conn.execute("SELECT * FROM recruiters").fetchall()

    conn.close()

    return render_template(
        'admin_recruiters.html',
        recruiters=recruiters
    )

@app.route('/admin_analytics')
def analytics():
    return render_template('admin_analytics.html')
@app.route('/admin_reports')
def reports():
    return render_template('admin_reports.html')

if __name__=='__main__':
    app.run(debug=True)