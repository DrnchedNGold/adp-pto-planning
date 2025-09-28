from .mongo import db
from bson import ObjectId

def get_employee_balance(employee_id: str) -> int:
    """
    Get remaining PTO balance for an employee.
    Accepts ObjectId or string (with or without 'employee_id:' prefix).
    """
    query_id = ObjectId(employee_id) if ObjectId.is_valid(employee_id) else employee_id
    employee = db.employees.find_one({"_id": query_id}, {"leave_balance": 1})
    return int(employee.get("leave_balance", 0)) if employee else 0

def get_employee_role(employee_id: str) -> str:
    employee = db.employees.find_one({"_id": ObjectId(employee_id)}, {"role": 1})
    return employee["role"] if employee else "Unknown"

if __name__ == "__main__":
    employee_id = '68d8c0500194311185f8d5d9'
    role = get_employee_role(employee_id)
    print(role)
