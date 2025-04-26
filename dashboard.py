import pyodbc
import os


base_dir = os.path.dirname(os.path.abspath(__file__))

db_file= os.path.join(base_dir, "PatientDatabase","patientapointdb.accdb")
# print("Full DB Path:", db_file)
# print("Exists:", os.path.exists(db_file))

db_file2 = os.path.join(base_dir, "Profile.accdb")

conn_str= (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    rf'DBQ={db_file};'
)
conn_str2= (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    rf'DBQ={db_file2};'
)

conn1 = pyodbc.connect(conn_str) #Connects to the PatientDatabase
cursor1 = conn1.cursor()

conn2 = pyodbc.connect(conn_str2)
cursor2 = conn2.cursor()

cursor1.execute("SELECT Name FROM MSysObjects WHERE Type=1 AND Flags=0;")
tables = cursor1.fetchall()
for table in tables:
    print(table[0])
#create a dashboard to show the data analytics
