from flask import Flask, render_template, request, redirect
import os

app=Flask(__name__)
UPLOAD_FOLDER='uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

# STUDENT DATA
student = {
    "name": "Anu",
    "email": "anu@gmail.com",
    "course": "BCA",
    "year": "3rd Year"
}

# JOB DATA
jobs=[
    {
        "company":"Infosys",
        "role":"Python Developer",
        "location":"Bangalore",
        "package":"5 LPA",
        "eligibility":"BCA/MCA"
    },
    {
        "company":"TCS",
        "role":"Web Developer",
        "location":"Kochi",
        "package":"4.5 LPA",
        "eligibility":"Any Degree"
    },
    {
        "company":"Wipro",
        "role":"Frontend Developer",
        "location":"Hyderabad",
        "package":"4 LPA",
        "eligibility":"BCA/BSc CS"
    }
]
# APPLICATION DATA
applications = []

# RESUME
resume_filename=""

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", applications=applications, jobs=jobs, resume_filename=resume_filename, student=student)

@app.route('/profile')
def profile():
    return render_template("profile.html", applications=applications, student=student, resume_filename=resume_filename)

@app.route('/jobs')
def jobs_page():
    return render_template("jobs.html", jobs=jobs, student=student, applications=applications)

@app.route('/job-details/<company>')
def job_details(company):
    selected_job=None
    for job in jobs:
        if job["company"]==company:
            selected_job=job
            break
    return render_template("job-details.html", job=selected_job, student=student, applications=applications)

@app.route('/update-profile', methods=['POST'])
def update_profile():
    if request.form['name']:
        student["name"] = request.form['name']
    if request.form['email']:
        student["email"] = request.form['email']
    if request.form['course']:
        student["course"] = request.form['course']
    if request.form['year']:
        student["year"] = request.form['year']
    return redirect('/profile')

@app.route('/apply/<company>', methods=['POST'])
def apply_job(company):
    if company not in applications:
        applications.append(company)
    return redirect('/profile')

@app.route('/remove-application/<company>', methods=['POST'])
def remove_application(company):
    if company in applications:
        applications.remove(company)
    return redirect('/profile')

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    global resume_filename
    file = request.files['resume']
    if file:
        resume_filename = file.filename 
        file.save(
            os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect('/profile')

if __name__=='__main__':
    app.run(debug=True)