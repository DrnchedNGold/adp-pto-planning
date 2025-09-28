from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from services import dashboard_employee
from db.mongo import db

router = APIRouter()

class DashboardRequest(BaseModel):
    email: str

@router.post("/employee_dashboard")
async def get_dashboard_data(request: DashboardRequest):
    employee = dashboard_employee.get_employee_by_email(request.email)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    policy = db.company_policies.find_one({"company_id": employee["company_id"]})
    if not policy:
        raise HTTPException(status_code=404, detail="Company policy not found")
    
    total_pto = policy.get("rules", {}).get("max_leave_days", 0)

    dashboard_data = {
        "employee_id": str(employee["_id"]),
        "team_id": str(employee.get("team_id")) if employee.get("team_id") else None,
        "manager_id": str(employee.get("manager_id")) if employee.get("manager_id") else None,
        "company_id": str(employee.get("company_id")) if employee.get("company_id") else None,
        "total_PTO": total_pto,
        "PTO_left": employee.get("leave_balance"),
    }
    return dashboard_data