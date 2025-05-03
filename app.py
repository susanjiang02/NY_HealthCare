from flask import Flask, request, jsonify, render_template, redirect
import pyodbc
import os
from appoinment_feature import create_appt

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(base_dir, "PatientDatabase", "patientapointdb.accdb")
conn_str = (
     r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    rf'DBQ={db_file};'
)

@app.route('/')
def root():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/appointments')
def index():
    conn1 = pyodbc.connect(conn_str)
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT PatientName, AppointmentDate, AppointmentTime, DoctorName, ReasonForVisit FROM Appointment")
    rows = cursor1.fetchall()
    conn1.close()

    appointments = [
        {
            "patient": row.PatientName,
            "date": row.AppointmentDate,
            "time": row.AppointmentTime,
            "doctor": row.DoctorName,
            "reason": row.ReasonForVisit
        } for row in rows
    ]
    return render_template('appointments.html', appointments= appointments)



@app.route('/book', methods=['POST'])
def book_appointment():
    patient_name = request.form.get('patient')
    appointment_date = request.form.get('date')
    appointment_time = request.form.get('time')
    doctor_name = request.form.get('doctor')
    reason_for_visit = request.form.get('reason')

    conn1 = pyodbc.connect(conn_str)
    cursor1 = conn1.cursor()

    cursor1.execute(''' 
        INSERT INTO Appointment(AppointmentDate, AppointmentTime, DoctorName, ReasonForVisit, PatientName)
        VALUES (?,?,?,?,?)
''', (appointment_date, appointment_time, doctor_name, reason_for_visit, patient_name))
    
    conn1.commit()
    conn1.close()

    return redirect('/appointments')

@app.route('/api/appointments')
def view_all_appointments():
    conn1 = pyodbc.connect(conn_str)
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT AppointmentDate, AppointmentTime, DoctorName, ReasonForVisit, PatientName FROM Appointment")
    rows = cursor1.fetchall()
    conn1.close()
    appointments = [
        {
            "patient": row.PatientName,
            "date": row.AppointmentDate,
            "time": row.AppointmentTime,
            "doctor": row.DoctorName,
            "reason": row.ReasonForVisit
        } for row in rows
    ]
    
    return jsonify(appointments)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')