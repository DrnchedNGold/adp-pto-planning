from langchain.agents import initialize_agent, AgentType
from .config import get_llm
from .utils import fetch_team_members, fetch_overlapping_leaves, fetch_employee_role

class CoverageAgent:
    def __init__(self):
        llm = get_llm()
        tools = [fetch_team_members, fetch_overlapping_leaves, fetch_employee_role]
        self.agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            handle_parsing_errors=True,
            verbose=True
        )

    def run(self, employee_id: str, team_id: str, leave_start: str, leave_end: str):
        query = f"""
        You are a Coverage Agent that evaluates whether a team can handle workload
        during a leave request. You have access to tools for fetching employee roles,
        team members, and overlapping leaves.

        Context:
        - Employee requesting leave: {employee_id}
        - Team ID: {team_id}
        - Leave period: {leave_start} → {leave_end}

        Strict workflow:
        1. Use fetch_employee_role to get the role of the requesting employee.
        2. Use fetch_team_members to get all team members and their roles.
        3. Use fetch_overlapping_leaves to get overlapping leaves for the same team
            and period. Exclude the requester’s leave.
        4. Check if at least one other team member with the same role is available
            (i.e., not on overlapping leave).
        5. Based on findings, compute a coverage_score:
            - 1.0 if there is full coverage
            - 0.5 if coverage is partial (reduced redundancy, but not critical)
            - 0.0 if no backup is available
        6. Prepare a list of uncovered_tasks (e.g., "No backup DevOps Engineer available").

        Output format:
        Return ONLY valid JSON in this schema:
        {{
            "coverage_score": float,
            "uncovered_tasks": [string]
        }}
        """
        return self.agent.invoke(query)

