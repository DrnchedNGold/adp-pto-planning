from langchain.tools import tool
from db.employees import get_employee_balance
from db.teams import get_blackout_dates

@tool
def fetch_leave_balance(employee_id: str) -> str:
    """Fetch an employee's remaining PTO balance."""
    return f"{get_employee_balance(employee_id)} days"

@tool
def fetch_blackout_dates(_) -> str:
    """Fetch company-wide blackout dates."""
    return str(get_blackout_dates())
