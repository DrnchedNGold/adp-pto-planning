from fastapi import APIRouter
from pydantic import BaseModel
from agents.orchestratorAgent import OrchestratorAgent

router = APIRouter()
orch = OrchestratorAgent()

class LeaveQueryRequest(BaseModel):
    employee_id: str
    company_id: str
    team_id: str
    query: str

@router.post("/leave-query")
def leave_query(request: LeaveQueryRequest):
    return orch.run(
        request.employee_id,
        request.company_id,
        request.team_id,
        request.query
    )
