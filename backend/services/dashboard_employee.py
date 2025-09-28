from db.mongo import db

def get_employee_by_email(email: str):
    employee = db.employees.find_one({"email": email})
    return employee
