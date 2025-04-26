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
def index():
    return render_template('appointments.html')



@app.route('/book', methods=['POST'])
def book_appointment():
    patient_name = request.form['patientName']
    doctor_name = request.form['doctor']
    date = request.form['date']
    time = request.form['time']
    reason = request.form['reason']

    conn1 = pyodbc.connect(conn_str)
    cursor1 = conn1.cursor()

    try:
        cursor1.execute('''
            INSERT INTO Appointment (AppointmentDate, AppointmentTime, ReasonForVisit, DoctorName, PatientName)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, time, reason, doctor_name, patient_name))
        conn1.commit()
        return redirect('/')
    except Exception as e:
        return f"An error occurred: {e}"