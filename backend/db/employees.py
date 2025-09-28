from .mongo import db

def get_employee_balance(employee_id: str) -> int:
    """
    Get remaining PTO balance for an employee.
    If no balance is stored, return 0.
    """
    employee = db.employees.find_one({"_id": employee_id}, {"leave_balance": 1})
    return employee.get("leave_balance", 0) if employee else 0
