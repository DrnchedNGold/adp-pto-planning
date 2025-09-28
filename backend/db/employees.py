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
