from langchain.tools import tool, StructuredTool
from pydantic import BaseModel, Field
from db.employees import get_employee_balance, get_employee_role
from db.policies import get_company_holidays
from db.teams import get_team_notices
from db.coverage import get_team_members_with_roles, get_overlapping_leaves

@tool
def fetch_employee_balance(employee_id: str) -> str:
    """Get the remaining PTO balance for an employee in days."""
    return str(get_employee_balance(employee_id))


@tool
def fetch_employee_role(employee_id: str) -> str:
    """Get the role of an employee (e.g., 'DevOps Engineer')."""
    return str(get_employee_role(employee_id))


@tool
def fetch_company_holidays(company_id: str) -> str:
    """Get company-wide holidays (e.g., Christmas)."""
    return str(get_company_holidays(company_id))


@tool
def fetch_team_notices(team_id: str) -> str:
    """Get blackout restrictions for a team (e.g., 'No PTO Jan 1–3')."""
    return str(get_team_notices(team_id))


@tool
def fetch_team_members(team_id: str) -> str:
    """Get team members and their roles."""
    members = get_team_members_with_roles(team_id)
    return str(members)


class OverlapInput(BaseModel):
    team_id: str = Field(..., description="Team ID")
    leave_start: str = Field(..., description="Leave start date in ISO format (YYYY-MM-DD or ISO timestamp)")
    leave_end: str = Field(..., description="Leave end date in ISO format (YYYY-MM-DD or ISO timestamp)")


def _fetch_overlapping_leaves(team_id: str, leave_start: str, leave_end: str) -> str:
    """Helper wrapper around DB function."""
    leaves = get_overlapping_leaves(team_id, leave_start, leave_end)
    return str(leaves)


fetch_overlapping_leaves = StructuredTool.from_function(
    func=_fetch_overlapping_leaves,
    name="fetch_overlapping_leaves",
    description="Get overlapping leaves in the given time window for a team.",
    args_schema=OverlapInput,
)