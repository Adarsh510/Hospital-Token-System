import sys
from app import app, db
from models import Department, Doctor, Appointment


def delete_row(model, row_id):
    with app.app_context():
        # Use Session.get() instead of Query.get()
        row = db.session.get(model, row_id)

        if row:
            if model == Department:
                # Delete all appointments related to doctors in the department
                doctors = Doctor.query.filter_by(department_id=row_id).all()
                for doctor in doctors:
                    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
                    for appointment in appointments:
                        db.session.delete(appointment)
                    db.session.delete(doctor)

            elif model == Doctor:
                # Delete all appointments related to the doctor
                appointments = Appointment.query.filter_by(doctor_id=row_id).all()
                for appointment in appointments:
                    db.session.delete(appointment)

            db.session.delete(row)
            db.session.commit()
            print(f"Row with ID {row_id} deleted from the '{model.__tablename__}' table.")
        else:
            print(f"No row found with ID {row_id} in the '{model.__tablename__}' table.")


if __name__ == "__main__":
    model_name = sys.argv[1]
    row_id = int(sys.argv[2])
    model_dict = {"Department": Department, "Doctor": Doctor, "Appointment": Appointment}
    delete_row(model_dict[model_name], row_id)
