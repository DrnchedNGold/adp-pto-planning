# backend/routes/dashboard_routes.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from services import leave_services

router = APIRouter()

class DashboardRequest(BaseModel):
    email: str

@router.post("/employee_dashboard")
async def get_dashboard_data(request: DashboardRequest):
    employee = leave_services.get_employee_by_email(request.email)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    dashboard_data = {
        "employee_id": str(employee["_id"]),
        "team_id": employee.get("team_id"),
        "manager_id": employee.get("manager_id"),
        "company_id": employee.get("company_id"),
        "total_PTO": employee.get("total_PTO"),
        "PTO_left": employee.get("PTO_left")
    }
    return dashboard_data
