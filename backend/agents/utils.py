from langchain.tools import tool
from db.employees import get_employee_balance
from db.policies import get_company_holidays
from db.teams import get_team_notices

@tool
def fetch_employee_balance(employee_id: str) -> str:
    """Get the remaining PTO balance for an employee in days."""
    return str(get_employee_balance(employee_id))

@tool
def fetch_company_holidays(company_id: str) -> str:
    """Get company-wide holidays (e.g., Christmas)."""
    return str(get_company_holidays(company_id))

@tool
def fetch_team_notices(team_id: str) -> str:
    """Get blackout restrictions for a team (e.g., 'No PTO Jan 1–3')."""
    return str(get_team_notices(team_id))
