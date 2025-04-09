import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect(':memory:') #creates temp
cursor = conn.cursor() #sql commands

cursor.execute(''' 
    CREATE TABLE Appointments(
               ID INTEGER PRIMARY KEY AUTOINCREMENT,
               PatientName TEXT NOT NULL,
               DoctorName TEXT NOT NULL,
               AppointmentDate DATE NOT NULL,
               AppointmentTime TEXT NOT NULL)
''')
conn.commit()


def create_appt(patient_name, doctor_name, date, time):
    try:
        time = datetime.strptime(time, '%H:%M').time()
    except ValueError:
        return 'Use 24 hour format.'
    
    if time < datetime.strptime('8:00', '%H:%M').time() or time > datetime.strptime('20:00', '%H:%M').time():
        return 'NY Health Clinic is only open 8AM - 8PM.'
    
    cursor.execute('SELECT * FROM Appointments WHERE DoctorName=? AND AppointmentDate=? AND AppointmentTime=?',
                   (doctor_name, date, time.strftime('%H:%M')))
    
    if cursor.fetchone():
        return 'Sorry that time is unavailable please select a different time.'
    
    cursor.execute('INSERT INTO Appointments (PatientName, DoctorName, AppointmentDate, AppointmentTime) VALUES (?,?,?,?)',
                   (patient_name, doctor_name, date, time.strftime('%H:%M')))
    conn.commit()

    return f"Appointment booked for {patient_name} with {doctor_name} at {time.strftime('%H:%M')} on {date}."

# patient_name = input('Enter your name: \n')
# doctor_name = input('The name of your doctor: \n')
# date = input('Enter the appointment date (YYYY-MM-DD): \n')
# time = input('Enter the time of the appointment (HH:MM): \n')
# test_result = create_appt(patient_name, doctor_name, date, time)
# print(test_result)


def cancel_appt(patient_name, doctor_name, date, time):
    try:
        time = datetime.strptime(time, '%H:%M').time()
    except ValueError:
        return 'Use a 24 hour time format please.'
    
    time_str = time.strftime('%H:%M')
    
    cursor.execute('''
        SELECT * FROM Appointments
        WHERE PatientName=? AND DoctorName=? AND AppointmentDate=? AND AppointmentTime=?
    ''', (patient_name, doctor_name, date, time_str))

    if not cursor.fetchone():
        return 'Could not find an appointment to cancel'
    
    cursor.execute('''
        DELETE FROM Appointments
        WHERE PatientName=? AND DoctorName=? AND AppointmentDate=? AND AppointmentTime=?
    ''', (patient_name, doctor_name, date, time_str))
    conn.commit()
    return f"Your appointment for {patient_name} at {time_str} on {date} has been cancelled."

def update_appt(patient_name, doctor_name, old_date, old_time, new_date, new_time):
    try:
        old_time = datetime.strptime(old_time, '%H:%M').time()
        new_time = datetime.strptime(new_time, '%H:%M').time()
    except ValueError:
        return 'Use a 24 hour time format please.'
    
    cursor.execute('''
        SELECT * FROM Appointments
        WHERE PatientName=? AND DoctorName=? AND AppointmentDate=? AND AppointmentTime=?
    ''', (patient_name, doctor_name, old_date, old_time.strftime('%H:%M')))
    if not cursor.fetchone():
        return 'Could not find an appointment.'
    
    cursor.execute('''
        SELECT * FROM Appointments
        WHERE DoctorName=? AND AppointmentDate=? AND AppointmentTime=?
    ''', (doctor_name, new_date, new_time.strftime('%H:%M')))
    if not cursor.fetchone():
        return 'That time is not available.'
    
    cursor.execute('''
        UPDATE Appointments
        SET AppointmentDate=?, AppointmentTime=?
        WHERE PatientName=? AND DoctorName=? AND AppointmentDate=? AND AppointmentTime=?
    ''', (new_date, new_time.strftime('%H:%M'), patient_name, doctor_name, old_date, old_time.strftime('%H:%M')))
    conn.commit()
    return f"Appointment had been updated from {old_time.strftime('%H:%M')} on {old_date} to {new_time.strftime('%H:%M')} on {new_date}."

# print(cancel_appointement('John Smith', 'DR. R', '2025-04-06', '10:00'))
# print(update_appointment('John Smith', 'DR. R', '2025-04-06', '10:00', '2025-04-09', '11:30'))
    
def view_all_appts(): #Data Analytics feature
    print('Here are all the appointments.')
    cursor.execute("SELECT * FROM Appointments")
    return cursor.fetchall()
    



