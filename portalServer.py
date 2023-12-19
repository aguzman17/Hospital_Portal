from datetime import datetime
from decimal import Decimal
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from portalDatabase import Database
import cgi
from os import curdir, sep

class HospitalPortalHandler(BaseHTTPRequestHandler):

    def __init__(self, *args):
        self.database = Database()
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_POST(self):
        try:
            if self.path == '/addPatient':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                patient_name = form.getvalue("patient_name")
                age = int(form.getvalue("patient_age"))
                admission_date = form.getvalue("admission_date")
                discharge_date = form.getvalue("discharge_date")

                # Call the Database Method to add a new patient.
                self.database.addPatient(patient_name, age, admission_date, discharge_date)

                print("Patient added:", patient_name, age, admission_date, discharge_date)

                self.display_success_page("Patient has been added", '/addPatient')

            elif self.path == '/scheduleAppointment':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                patient_id = int(form.getvalue("patient_id"))
                doctor_id = int(form.getvalue("doctor_id"))
                appointment_date = form.getvalue("appointment_date")
                appointment_time = Decimal(form.getvalue("appointment_time"))

                # Call the Database Method to schedule an appointment.
                self.database.scheduleAppointment(patient_id, doctor_id, appointment_date, appointment_time)

                self.display_success_page("Appointment has been scheduled", '/scheduleAppointment')

            elif self.path == '/dischargePatient':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                patient_id = int(form.getvalue("patient_id"))

                # Call the Database Method to discharge a patient.
                self.database.dischargePatient(patient_id)

                self.display_success_page("Patient has been discharged", '/dischargePatient')
       
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

        return

    def do_GET(self):
        try:
            if self.path == '/':
                data = []
                records = self.database.getAllPatients()
                print(records)
                data = records
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head>")
                self.wfile.write(b"<link rel='stylesheet' type='text/css' href='/styles.css'>")
                self.wfile.write(b"<title>Hospital's Portal</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.display_navigation_links()
                self.wfile.write(b"<hr><h2>All Patients</h2>")
                self.display_patient_table(data)
                self.wfile.write(b"</body></html>")
                return
            
            elif self.path == '/addPatient':
                #Displaying the add patient form
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head>")
                self.wfile.write(b"<link rel='stylesheet' type='text/css' href='/styles.css'>")
                self.wfile.write(b"<title>Hospital's Portal</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.display_navigation_links()
                self.wfile.write(b"<hr><h2>Add New Patient</h2>")
                self.display_add_patient_form()
                self.wfile.write(b"</center></body></html>")
                return
            
            elif self.path == '/scheduleAppointment':
                #Displaying the scheduling appointment form
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head>")
                self.wfile.write(b"<link rel='stylesheet' type='text/css' href='/styles.css'>")
                self.wfile.write(b"<title>Hospital's Portal</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.display_navigation_links()
                self.wfile.write(b"<hr><h2>Schedule Appointment</h2>")
                self.display_schedule_appointment_form()
                self.wfile.write(b"</center></body></html>")

            elif self.path == '/viewAppointments':
                #Displaying all appointments
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head>")
                self.wfile.write(b"<link rel='stylesheet' type='text/css' href='/styles.css'>")
                self.wfile.write(b"<title>Hospital's Portal</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.display_navigation_links()
                self.wfile.write(b"<hr><h2>View Appointments</h2>")
                self.display_view_appointments()
                self.wfile.write(b"</center></body></html>")

            elif self.path == '/dischargePatient':
                #Displaying the discharge patient form
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head>")
                self.wfile.write(b"<link rel='stylesheet' type='text/css' href='/styles.css'>")
                self.wfile.write(b"<title>Hospital's Portal</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Hospital's Portal</h1>")
                self.wfile.write(b"<hr>")
                self.display_navigation_links()
                self.wfile.write(b"<hr><h2>Discharge Patient</h2>")
                self.display_discharge_patient_form()
                self.wfile.write(b"</center></body></html>")

            if self.path.endswith('.css'):
                css_path = curdir + sep + 'styles.css'
                with open(css_path, 'rb') as css_file:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/css')
                    self.end_headers()
                    self.wfile.write(css_file.read())

        except IOError as e:
            print("IOError:", e)
            self.send_error(404, 'File Not Found: %s' % self.path)

        return   

    # Helper methods

    def display_success_page(self, message, back_link):
        self.wfile.write(b"<html><head>")
        self.wfile.write(b"<link rel='stylesheet' type='text/css' href='/styles.css'>")
        self.wfile.write(b"<title>Hospital's Portal</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Hospital Portal</h1>")
        self.wfile.write(b"<hr>")
        self.display_navigation_links()
        self.wfile.write(f"<hr><h3>{message}</h3>")
        self.wfile.write(f"<a href='{back_link}'>Back</a>")
        self.wfile.write(b"</center></body></html>")

    def display_navigation_links(self):
        links = [
            ('Home', '/'),
            ('Add Patient', '/addPatient'),
            ('Schedule Appointment', '/scheduleAppointment'),
            ('View Appointments', '/viewAppointments'),
            ('Discharge Patient', '/dischargePatient'),
        ]

        self.wfile.write(b"<div id='menu'>")
        for link_text, link_url in links:
            self.wfile.write(f"<a href='{link_url}'>{link_text}</a>".encode())
            #self.wfile.write(b" | ")
        self.wfile.write(b"</div>")

    def display_patient_table(self, data):
        self.wfile.write(b"<table border=2> \
                            <tr><th> Patient ID </th>\
                                <th> Patient Name</th>\
                                <th> Age </th>\
                                <th> Admission Date </th>\
                                <th> Discharge Date </th></tr>")
        for row in data:
            self.wfile.write(b' <tr> <td>')
            self.wfile.write(str(row[0]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[1]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[2]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[3]).encode())
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[4]).encode())
            self.wfile.write(b'</td></tr>')

        self.wfile.write(b"</table>")

    def display_add_patient_form(self):
        self.wfile.write(b"<form action='/addPatient' method='post'>")
        self.wfile.write(b'''<form action='/addPatient' method='post'>
            <label for="patient_name">Patient Name:</label>
            <input type="text" id="patient_name" name="patient_name"/><br><br>
            <label for="patient_age">Age:</label>
            <input type="number" id="patient_age" name="patient_age"><br><br>
            <label for="admission_date">Admission Date:</label>
            <input type="date" id="admission_date" name="admission_date"><br><br>
            <label for="discharge_date">Discharge Date:</label>
            <input type="date" id="discharge_date" name="discharge_date"><br><br>
            <input type="submit" value="Submit">
        </form>''')

    def display_schedule_appointment_form(self):
        self.wfile.write(b"<form action='/scheduleAppointment' method='post'>")
        self.wfile.write(b'''<form action='/scheduleAppointment' method='post'>
            <label for="patient_id">Patient ID:</label>
            <input type="number" id="patient_id" name="patient_id"/><br><br>
            <label for="doctor_id">Doctor ID:</label>
            <input type="number" id="doctor_id" name="doctor_id"><br><br>
            <label for="appointment_date">Appointment Date:</label>
            <input type="date" id="appointment_date" name="appointment_date"><br><br>
            <label for="appointment_time">Appointment Time:</label>
            <input type="text" id="appointment_time" name="appointment_time" placeholder="HH.MM"><br><br>
            <input type="submit" value="Submit">
        </form>''')

    def display_view_appointments(self):
        #displaying all appointments
        appointments = self.database.viewAppointments()
        self.wfile.write(b"<table border=2>")
        self.wfile.write(b"<tr>"
                        b"<th> Appointment ID </th>"
                        b"<th> Patient Name</th>"
                        b"<th> Doctor Name </th>"
                        b"<th> Appointment Date </th>"
                        b"<th> Appointment Time </th>"
                        b"</tr>")

        for row in appointments:
            self.wfile.write(b' <tr> <td>')
            self.wfile.write(str(row[0]).encode())  # Appointment ID
            self.wfile.write(b'</td><td>')

            if len(row) > 4:
                self.wfile.write(str(row[4]).encode())  # Patient Name
            else:
                self.wfile.write(b'N/A')

            self.wfile.write(b'</td><td>')

            if len(row) > 9:
                self.wfile.write(str(row[9]).encode())  # Doctor Name
            else:
                self.wfile.write(b'N/A')

            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[1]).encode())  # Appointment Date
            self.wfile.write(b'</td><td>')
            self.wfile.write(str(row[2]).encode())  # Appointment Time
            self.wfile.write(b'</td></tr>')

        self.wfile.write(b"</table>")

    def display_discharge_patient_form(self):
        self.wfile.write(b"<form action='/dischargePatient' method='post'>")
        self.wfile.write(b'''<form action='/dischargePatient' method='post'>
            <label for="patient_id">Patient ID:</label>
            <input type="number" id="patient_id" name="patient_id"/><br><br>
            <input type="submit" value="Submit">
        </form>''')

    def display_all_tables(self, data):
        self.wfile.write(b"<table border=2>")
        for row in data:
            self.wfile.write(b' <tr>')
            for item in row:
                self.wfile.write(b'<td>')
                self.wfile.write(str(item).encode())
                self.wfile.write(b'</td>')
            self.wfile.write(b'</tr>')
        self.wfile.write(b"</table>")

    def display_doctors_table(self, data):
        self.wfile.write(b"<table border=2>")
        for row in data:
            self.wfile.write(b' <tr>')
            for item in row:
                self.wfile.write(b'<td>')
                self.wfile.write(str(item).encode())
                self.wfile.write(b'</td>')
            self.wfile.write(b'</tr>')
        self.wfile.write(b"</table>")

    def display_records_table(self, data):
        self.wfile.write(b"<table border=2>")
        for row in data:
            self.wfile.write(b' <tr>')
            for item in row:
                self.wfile.write(b'<td>')
                self.wfile.write(str(item).encode())
                self.wfile.write(b'</td>')
            self.wfile.write(b'</tr>')
        self.wfile.write(b"</table>")

def run(server_class=HTTPServer, handler_class=HospitalPortalHandler, port=8000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()

run()
