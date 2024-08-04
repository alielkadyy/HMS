from flask import Flask, render_template, request, redirect, url_for, flash, session
import pyodbc
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a real secret key

def get_db_connection():
    connection_string = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=AHMED\SQLEXPRESS;'
        'DATABASE=HMS1;'
        'Trusted_Connection=yes;'
    )
    conn = pyodbc.connect(connection_string)
    return conn

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

@app.route('/admin-panel1.html')
def admin():
    return render_template('admin-panel1.html')

@app.route('/logout.html')
def logout():
    return render_template('logout.html')

@app.route('/logout1.html')
def logout1():
    return render_template('logout1.html')

if __name__ == '__main__':
    app.run(debug=True)
