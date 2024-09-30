from app import app, db
from models import Department, Doctor

def add_sample_data():
    with app.app_context():
        # Sample data to insert
        departments = ['Cardiology', 'Neurology', 'Orthopedics']
        doctors = [
            {'name': 'Dr. Smith', 'department': 'Cardiology'},
            {'name': 'Dr. Johnson', 'department': 'Neurology'},
            {'name': 'Dr. Lee', 'department': 'Orthopedics'}
        ]

        # Add departments
        for dept_name in departments:
            if not Department.query.filter_by(name=dept_name).first():
                new_department = Department(name=dept_name)
                db.session.add(new_department)

        # Commit after adding departments
        db.session.commit()

        # Add doctors
        for doc in doctors:
            department = Department.query.filter_by(name=doc['department']).first()
            if department:
                if not Doctor.query.filter_by(name=doc['name']).first():
                    new_doctor = Doctor(name=doc['name'], department_id=department.id)
                    db.session.add(new_doctor)

        # Commit after adding doctors
        db.session.commit()
        print("Sample data added successfully.")

if __name__ == "__main__":
    add_sample_data()
