from flask import Flask, render_template, request, redirect, url_for, flash, session
import pyodbc
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_unique_secret_key'

def get_db_connection():
    connection_string = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=MOTAZ-PC\SQLEXPRESS;'
        'DATABASE=HMS;'
        'Trusted_Connection=yes;'
    )
    conn = pyodbc.connect(connection_string)
    return conn

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form.get('fname')
    last_name = request.form.get('lname')
    gender = request.form.get('gender')
    email = request.form.get('email')
    contact = request.form.get('contact')
    password = request.form.get('password')
    role = 'Patient'  # Always 'Patient'
    specialization = ''  # Empty specialization

    conn = get_db_connection()  # Get a database connection
    cursor = conn.cursor()  # Create a cursor object

    # Insert data into the Users table
    cursor.execute("""
        INSERT INTO Users (first_name, last_name, gender, email, contact, password, role, specialization)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (first_name, last_name, gender, email, contact, password, role, specialization))
    
    conn.commit()
    cursor.close()  # Close the cursor
    conn.close()  # Close the connection
    
    return redirect(url_for('index'))  # Redirect to a success page or another relevant route

@app.route('/login_doctor', methods=['POST'])
def login_doctor():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE email = ? AND password = ? AND role = ?', (email, password, 'Doctor'))
    user = cursor.fetchone()
    conn.close()

    if user:
        return redirect(url_for('doctor'))  # Replace with actual doctor dashboard route
    else:
        return render_template('index.html', error_message_doctor='Wrong Email/Password')
    
@app.route('/login_admin', methods=['POST'])
def login_admin():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE email = ? AND password = ? AND role = ?', (email, password, 'Admin'))
    user = cursor.fetchone()
    conn.close()

    if user:
        return redirect(url_for('admin'))  # Replace with actual admin dashboard route
    else:
        return render_template('index.html', error_message_admin='Wrong Email/Password')

def register():
    first_name = request.form['fname']
    last_name = request.form['lname']
    gender = request.form['gender']
    email = request.form['email']
    contact = request.form['contact']
    password = request.form['password']
    cpassword = request.form['cpassword']

    if password != cpassword:
        return 'Passwords do not match!'

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Users (first_name, last_name, gender, email, contact, password, role, specialization) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (first_name, last_name, gender, email, contact, password, 'Patient', ''))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/admin-panel1.html')
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DoctorList")
    doctors = cursor.fetchall()

    cursor.execute("PatientList")
    patients = cursor.fetchall()

    cursor.execute("AppointmentDetails")
    appointments = cursor.fetchall()

    cursor.execute("PrescriptionList")
    prescriptions = cursor.fetchall()
    conn.close()
    return render_template('admin-panel1.html', doctors=doctors,patients=patients,appointments=appointments,prescriptions=prescriptions)

@app.route('/delete-doctor', methods=['POST'])
def delete_doctor():
    email = request.form['demail']
    
    if not email:
        flash('Email is required!')
        return redirect(url_for('admin_panel'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # SQL query to delete the doctor with the given email
        cursor.execute('DELETE FROM users WHERE email = ? AND role = ?', (email, 'Doctor'))
        conn.commit()


        # Check if the deletion was successful
        if cursor.rowcount == 0:
            flash('No doctor found with that email address.')
        else:
            flash('Doctor deleted successfully.')

    except Exception as e:
        conn.rollback()
        flash(f'An error occurred: {str(e)}')
    
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('admin'))

@app.route('/admin-panel1.html', methods=['POST'])
def add_doctor():
    # Retrieve form data
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    gender = request.form.get('gender')
    email = request.form.get('email')
    contact = request.form.get('contact')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    specialization = request.form.get('specialization')


    if password != confirm_password:
        return 'Passwords do not match!'

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert the form data into the database
    cursor.execute('INSERT INTO users (first_name, last_name, gender, email, contact, password, role, specialization) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (first_name, last_name, gender, email, contact, password, 'Doctor', specialization))
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

    return redirect(url_for('admin'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query to check user credentials
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ? AND role = ?', (email, password, 'patient'))
    user = cursor.fetchone()

    conn.close()

    if user:
        return redirect(url_for('patient'))  # Redirect to the patient panel
    else:
        flash('Invalid email or password', 'error')
        return redirect(url_for('index1'))  # Redirect back to login page
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/index1.html')
def index1():
    return render_template('index1.html')

@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form['txtName']
            email = request.form['txtEmail']
            phone = request.form['txtPhone']
            message = request.form['txtMsg']
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            conn = get_db_connection()
            cur = conn.cursor()
            
            query = """
            INSERT INTO ContactMessages (name, Contact, email, message, date)
            VALUES (?, ?, ?, ?, ?)
            """
            cur.execute(query, (name, phone, email, message, date))
            conn.commit()
            cur.close()
            conn.close()
            
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred while sending your message: {e}', 'danger')
            print(e)
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/services.html')
def services():
    return render_template('services.html')

@app.route('/doctor-panel.html')
def doctor():
    return render_template('doctor-panel.html')

@app.route('/patient-panel.html')
def patient():
    return render_template('patient-panel.html')
  
@app.route('/logout.html')
def logout():
    return render_template('logout.html')

@app.route('/logout1.html')
def logout1():
    return render_template('logout1.html')

if __name__ == '__main__':
    app.run(debug=True)
