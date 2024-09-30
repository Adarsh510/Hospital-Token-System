import sys
from app import app, db
from models import Department, Doctor, Appointment  # Import all models

def clear_table(model):
    with app.app_context():
        db.session.query(model).delete()
        db.session.commit()
        print(f"All records from the '{model.__tablename__}' table have been deleted.")

if __name__ == "__main__":
    model_name = sys.argv[1]
    model_dict = {"Department": Department, "Doctor": Doctor, "Appointment": Appointment}
    clear_table(model_dict[model_name])
