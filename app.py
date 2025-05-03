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
    cursor1.execute("SELECT AppointmentID, PatientName, AppointmentDate, AppointmentTime, DoctorName, ReasonForVisit FROM Appointment")
    rows = cursor1.fetchall()
    # conn1.close()

    appointments = [  #gets appt info
        {
            "patient": row.PatientName,
            "date": row.AppointmentDate,
            "time": row.AppointmentTime,
            "doctor": row.DoctorName,
            "reason": row.ReasonForVisit
        } for row in rows
    ]
        #get doctor info
    cursor1.execute("SELECT LastName FROM Doctor")
    doctor_rows = cursor1.fetchall()
    doctors = [row.LastName for row in doctor_rows]
    conn1.close()

    return render_template('appointments.html', appointments= appointments, doctors=doctors)



@app.route('/book', methods=['POST'])
def book_appointment():
    data = request.get_json()
    patient_name = data.get('patient')
    appointment_date = data.get('date')
    appointment_time = data.get('time')
    doctor_name = data.get('doctor')
    reason_for_visit = data.get('reason')

    conn1 = pyodbc.connect(conn_str)
    cursor1 = conn1.cursor()

    cursor1.execute(''' 
        INSERT INTO Appointment(AppointmentDate, AppointmentTime, DoctorName, ReasonForVisit, PatientName)
        VALUES (?,?,?,?,?)
''', (appointment_date, appointment_time, doctor_name, reason_for_visit, patient_name))
    
    conn1.commit()
    conn1.close()

    return jsonify({"message": "Appointment has been booked."}), 200

@app.route('/api/appointments')
def view_all_appointments():
    conn1 = pyodbc.connect(conn_str)
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT AppointmentID, AppointmentDate, AppointmentTime, DoctorName, ReasonForVisit, PatientName FROM Appointment")
    rows = cursor1.fetchall()
    conn1.close()
    appointments = [
        {
            "AppointmentID": row.AppointmentID,
            "patient": row.PatientName,
            "date": row.AppointmentDate,
            "time": row.AppointmentTime,
            "doctor": row.DoctorName,
            "reason": row.ReasonForVisit
        } for row in rows
    ]
    # print(appointments)
    return jsonify(appointments)

@app.route('/delete/<int:appointment_id>', methods=['DELETE'])
def delete_appt(appointment_id):
    conn1 = pyodbc.connect(conn_str)
    cursor1 = conn1.cursor()
    try:
        cursor1.execute("DELETE FROM Appointment WHERE AppointmentID = ?", (appointment_id,))
        conn1.commit()
        return '', 204
    except Exception as e:
        print('Was not able to delete the appointment.', e)
        return 'Could not delete', 500
    finally:
        conn1.close()
   

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')