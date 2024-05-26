import os
import sqlite3
import re
from flask import Flask, render_template, request, redirect, url_for, flash, g, session

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.database = 'example2.db'

def connect_db():
    return sqlite3.connect(app.database)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

def is_valid_gitam_email(email):
    pattern = r'@gitam\.in$'
    return re.search(pattern, email)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = g.db.execute('SELECT registration_number, email, student_name FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        if user:
            session['user'] = user[1]
            session['student_name'] = user[2]  # Using student_name instead of username
            session['registration_number'] = user[0]
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, please try again.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('student_name', None)
    session.pop('registration_number', None)  # Clear the registration number from the session
    flash('Logout successful', 'success')
    return redirect(url_for('login'))

@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form['email']
        flash('Password reset email sent successfully', 'success')
        return redirect(url_for('login'))
    return render_template('forget_password.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        if not is_valid_gitam_email(email):
            flash('Please enter your Gitam email id.', 'error')
            return redirect(url_for('signup'))
        student_name = request.form['student_name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('signup'))
        g.db.execute('INSERT INTO users (email, student_name, password) VALUES (?, ?, ?)', (email, student_name, password))
        g.db.commit()
        flash('Signup successful', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', student_name=session['student_name'])
    else:
        flash('You need to login first', 'error')
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'user' in session:
        return render_template('profile.html')
    else:
        flash('You need to login first', 'error')
        return redirect(url_for('login'))

def get_courses():
    with sqlite3.connect('example2.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT course_name, course_description FROM courses')
        courses = cursor.fetchall()
    return [{'course_name': row[0], 'course_description': row[1]} for row in courses]

@app.route('/courses')
def courses():
    if 'user' in session:
        courses = get_courses()
        return render_template('courses.html', courses=courses)
    else:
        flash('You need to login first', 'error')
        return redirect(url_for('login'))

def get_grades(registration_number):
    with sqlite3.connect('example2.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT semester, sgpa, cgpa 
            FROM grades 
            WHERE registration_number = ?
            ORDER BY semester
        ''', (registration_number,))
        grades = cursor.fetchall()
    return [{'semester': row[0], 'sgpa': row[1], 'cgpa': row[2]} for row in grades]

@app.route('/grades')
def grades():
    if 'user' in session:
        registration_number = session['registration_number']
        grades = get_grades(registration_number)
        return render_template('grades.html', grades=grades)
    else:
        flash('You need to login first', 'error')
        return redirect(url_for('login'))

@app.route('/attendance')
def attendance():
    if 'user' in session:
        return render_template('attendance.html')
    else:
        flash('You need to login first', 'error')
        return redirect(url_for('login'))

@app.route('/timetable')
def timetable():
    if 'user' in session:
        return render_template('timetable.html')
    else:
        flash('You need to login first', 'error')
        return redirect(url_for('login'))

@app.route('/messages')
def messages():
    if 'user' in session:
        return render_template('messages.html')
    else:
        flash('You need to login first', 'error')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
