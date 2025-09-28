from fastapi import APIRouter, Query
from agents.orchestratorAgent import OrchestratorAgent

router = APIRouter()
orch = OrchestratorAgent()

@router.post("/leave-query")
def leave_query(
    employee_id: str = Query(...),
    company_id: str = Query(...),
    team_id: str = Query(...),
    query: str = Query(...)
):
    """
    Handle a leave request or chatbot query.
    """
    return orch.run(employee_id, company_id, team_id, query)
