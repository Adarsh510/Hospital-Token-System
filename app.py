from flask import Flask, request, jsonify, render_template
from models import db, Department, Doctor, Appointment

app = Flask(__name__, template_folder='templates')

# Use absolute path for SQLite database URI
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance/hospital.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        department_name = request.form['department']
        name = request.form['name']
        mobile = request.form['mobile']

        department = Department.query.filter_by(name=department_name).first()
        if not department:
            return jsonify({"error": "Department not found."}), 404

        doctor = Doctor.query.filter_by(department_id=department.id).first()
        if not doctor:
            return jsonify({"error": "Doctor not found for this department."}), 404

        last_appointment = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.token_number.desc()).first()
        next_token_number = last_appointment.token_number + 1 if last_appointment else 1

        new_appointment = Appointment(name=name, mobile=mobile, token_number=next_token_number, doctor_id=doctor.id)
        db.session.add(new_appointment)
        db.session.commit()

        return jsonify({"message": "Appointment booked successfully!", "token_number": next_token_number})

    return render_template('book_appointment.html')

@app.route('/search_appointments', methods=['GET', 'POST'])
def search_appointments():
    if request.method == 'POST':
        search_term = request.form['search']
        appointments = Appointment.query.filter(
            (Appointment.name.like(f"%{search_term}%")) | (Appointment.mobile.like(f"%{search_term}%"))
        ).all()

        appointments_list = [
            {
                "name": appt.name,
                "mobile": appt.mobile,
                "token_number": appt.token_number,
                "doctor_name": appt.doctor.name,
                "department_name": appt.doctor.department.name
            } for appt in appointments
        ]

        return jsonify(appointments_list)

    return render_template('search_appointments.html')

if __name__ == "__main__":
    app.run(debug=True)
