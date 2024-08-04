from flask import Flask, render_template
import pyodbc


app = Flask(__name__)

def get_db_connection(): # you will need to change the Server name to yours
    connection_string = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-NOS3O0I;'
        'DATABASE=HMS;'
        'Trusted_Connection=yes;'
    )
    conn = pyodbc.connect(connection_string)
    return conn

conn = get_db_connection()
cur = conn.cursor()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/index1.html')
def index1():
    return render_template('index1.html')

@app.route('/contact.html')
def contact():
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
