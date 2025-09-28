from langchain.agents import initialize_agent, AgentType
from .config import get_llm
from .utils import fetch_employee_balance, fetch_company_holidays, fetch_team_notices

class PolicyAgent:
    def __init__(self):
        llm = get_llm()
        tools = [fetch_employee_balance, fetch_company_holidays, fetch_team_notices]
        self.agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            verbose=True
        )

    def run(self, employee_id: str, company_id: str, team_id: str, leave_start: str, leave_end: str):
        query = f"""
        You are a Policy Agent that evaluates leave requests.

        Employee: {employee_id}
        Company: {company_id}
        Team: {team_id}
        Requested leave: {leave_start} → {leave_end}

        1. Call tools to fetch PTO balance, holidays, and team notices.
        2. Use those facts to decide if the leave violates any rules.
        3. Return ONLY JSON in this format:

        {{
          "policy_score": float (0.0 → 1.0),
          "notes": "short reasoning about PTO balance, holidays, and blackout rules"
        }}
        """
        return self.agent.run(query)
