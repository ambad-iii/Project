from flask import Flask, render_template,request,redirect
app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')
@app.route('/students')
def students():
    return render_template('students.html')
@app.route('/recruiters')
def recruiters():
    return render_template('recruiters.html')
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')
@app.route('/reports')
def reports():
    return render_template('reports.html')
if __name__ == '__main__':
    app.run(debug=True)
