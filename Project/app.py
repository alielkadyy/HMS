from flask import Flask, request, redirect, url_for, render_template, flash, session,jsonify, request,get_flashed_messages
import pyodbc
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_unique_secret_key'

def get_db_connection():
    connection_string = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=YOUSSEF-ATEF\SQLEXPRESS;'
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
    cpassword = request.form.get('cpassword')

    if password != cpassword:
        return 'Passwords do not match!'

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Users (first_name, last_name, gender, email, contact, password, role, specialization) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (first_name, last_name, gender, email, contact, password, 'Patient', ''))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/login_doctor', methods=['POST'])
def login_doctor():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE email = ? AND password = ? AND role = ?', (email, password, 'Doctor'))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        session['user_id'] = user[0]  # Assuming the first column is the user ID
        session['role'] = user[7]
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
    cursor.close()
    conn.close()

    if user:
        session['user_id'] = user[0]
        session['role'] = user[7]
        return redirect(url_for('admin'))  # Replace with actual admin dashboard route
    else:
        return render_template('index.html', error_message_admin='Wrong Email/Password')

@app.route('/admin-panel1.html')
def admin():
    admin_id = session['user_id']
    Role = session['role']
    if admin_id and Role == 'Admin':
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

        cursor.execute("SELECT name , email , contact , message FROM ContactMessages")
        messages = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return render_template('admin-panel1.html', doctors=doctors, patients=patients, appointments=appointments, prescriptions=prescriptions ,messages=messages)
    else:
        return redirect(url_for('index'))


@app.route('/delete-doctor', methods=['POST'])
def delete_doctor():
    email = request.form['demail']

    if not email:
        flash('Email is required!')
        return redirect(url_for('admin'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM Users WHERE email = ? AND role = ?', (email, 'Doctor'))
        conn.commit()

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

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Users (first_name, last_name, gender, email, contact, password, role, specialization) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (first_name, last_name, gender, email, contact, password, 'Doctor', specialization))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Users WHERE email = ? AND password = ? AND role = ?', (email, password, 'Patient'))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        session['user_id'] = user[0]  # Assuming the first column is the user ID
        session['role'] = user[7]
        return redirect(url_for('patient_panel'))  # Redirect to the patient panel
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
    doctor_id = session['user_id']   # Replace this with the actual doctor ID from the session
    Role = session['role']
    if doctor_id and Role == 'Doctor':
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('EXEC AppointmentDetailsFromDoctor ?',doctor_id)
        app_list = cursor.fetchall()

        cursor.execute("SELECT concat(first_name , ' ' , last_name) FROM USERS WHERE user_id = ?" , doctor_id)
        username = cursor.fetchone()

        cursor.execute('EXEC PrescriptionsDetailsFromDoctor ?',doctor_id)
        pr_list = cursor.fetchall()



        conn.close()
        return render_template('doctor-panel.html', app_list=app_list, username=username, pr_list=pr_list )
    else:
        return redirect(url_for('index'))

@app.route('/prescribe.html')
def prescribe():

    doctor_id = session['user_id']   # Replace this with the actual doctor ID from the session
    Role = session['role']
    if doctor_id and Role == 'Doctor':
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT concat(first_name , ' ' , last_name) FROM USERS WHERE user_id = ?" , doctor_id)
        username = cursor.fetchone()


        cursor.close()
        conn.close()
    else:
       return redirect(url_for('index1')) 
    return render_template('prescribe.html' , username=username)

@app.route('/patient-panel.html', methods=['GET', 'POST'])
def patient_panel():
    patientId = session['user_id']
    Role = session['role']

    if patientId and Role == 'Patient':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT concat(first_name, ' ', last_name) FROM USERS WHERE user_id = ?", patientId)
        username = cursor.fetchone()

        # Fetch appointment history
        cursor.execute("EXEC AppointmentHistoryForSpecificPatient ?", patientId)
        appointments = cursor.fetchall()

        # Fetch prescriptions
        cursor.execute("EXEC ViewPrescriptionForSpecificPatient ?", patientId)
        prescription = cursor.fetchall()

        # Handle form submission for doctor selection
        if request.method == 'POST':
            selected_specialization = request.form.get('specialization')
            if selected_specialization:
                cursor.execute("SELECT user_id, concat(first_name, ' ', last_name) FROM USERS WHERE specialization = ?", selected_specialization)
                doctorList = cursor.fetchall()
            else:
                doctorList = []
        else:
            cursor.execute("SELECT DISTINCT specialization FROM USERS WHERE specialization != ''")
            spec = cursor.fetchall()
            doctorList = []
        cursor.close()
        conn.close()
    else:
        return redirect(url_for('index1'))

    

    return render_template('patient-panel.html', appointments=appointments, prescription=prescription, username=username, spec=spec, doctorList=doctorList)

@app.route('/get-doctors', methods=['POST'])
def get_doctors():
    specialization = request.form.get('specialization')
    if not specialization:
        return jsonify({'error': 'Specialization not provided'}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT user_id, concat(first_name, ' ', last_name)
            FROM USERS
            WHERE role = 'Doctor' AND specialization = ?
        """
        cursor.execute(query, (specialization,))
        doctors = cursor.fetchall()

        cursor.close()
        conn.close()

        # Convert tuple list to a list of dictionaries for JSON serialization
        doctors_list = [{'user_id': doctor[0], 'name': doctor[1]} for doctor in doctors]
        
        return jsonify(doctors_list)
    except Exception:
        return jsonify({'error': 'An internal error occurred'}), 500

@app.route('/create-appointment', methods=['POST'])
def create_appointment():
    # Get form data
    specialization = request.form.get('SelectSpecilization')
    doctor_name = request.form.get('doctors')
    appointment_date = request.form.get('appdate')
    appointment_time = request.form.get('apptime')
    consultancy_fees = 250  # Fixed value

    # Get the current patient ID
    patient_id = session.get('user_id')
    if not patient_id:
        return "User not logged in."

    # Debug print for doctor_name
    print(f"Doctor Name to query: {doctor_name}")

    # Get doctor_id from the users table
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM DoctorView WHERE full_name = ?;", (doctor_name,))
    result = cursor.fetchone()

    if result:
        doctor_id = result[0]
    else:
        conn.close()
        return "Doctor not found. Please select a valid doctor."

    # Insert into appointments table
    cursor.execute(
        "INSERT INTO Appointments (date, status, patient_id, doctor_id) VALUES (?, 'Pending', ?, ?)",
        (f"{appointment_date} {appointment_time}", patient_id, doctor_id)
    )
    conn.commit()
    conn.close()

    # Flash a success message
    flash('Appointment set successfully!')
    return redirect(url_for('patient_panel'))

@app.route('/cancel-appointment/<int:appointment_id>', methods=['POST'])
def cancel_appointment(appointment_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Appointments 
            SET status = 'Cancelled by Patient' 
            WHERE appointment_id = ?
        """, (appointment_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False}), 500
    
    
@app.route('/bill_template.html')
def Payment():
    patientId = session['user_id']
    Role = session['role']

    if patientId and Role == 'Patient':
      return render_template('bill_template.html')


@app.route('/logout.html')
def logout():
    session['role']=''
    session['user_id'] =  0
    return render_template('logout.html')

@app.route('/logout1.html')
def logout1():
    session['role']=''
    session['user_id'] =  0
    return render_template('logout1.html')

if __name__ == '__main__':
    app.run(debug=True)