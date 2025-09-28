from dateutil import parser
from datetime import datetime, timezone
import re
from .policy_agent import PolicyAgent
from .coverage_agent import CoverageAgent
from .config import get_llm
import json
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain


class OrchestratorAgent:
    def __init__(self):
        self.llm = get_llm()

        # still classify intent so chatbot queries are handled
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Classify user query into either 'leave_request' or 'chatbot'."),
            ("user", "{query}")
        ])
        self.classifier = LLMChain(llm=self.llm, prompt=prompt)

    def classify_intent(self, query: str) -> str:
        result = self.classifier.run(query)
        return "leave_request" if "leave_request" in result.lower() else "chatbot"

    def extract_dates(self, query: str):
        matches = re.findall(
            r"(?:\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2}(?:st|nd|rd|th)?)",
            query,
            re.IGNORECASE
        )
        dates = []
        for match in matches:
            try:
                parsed = parser.parse(
                    match,
                    fuzzy=True,
                    default=datetime(datetime.now().year, 1, 1, tzinfo=timezone.utc)
                )
                parsed = parsed.replace(tzinfo=timezone.utc)
                dates.append(parsed.isoformat(timespec="milliseconds"))
            except Exception:
                continue
        if len(dates) == 1:
            return dates[0], dates[0]
        elif len(dates) >= 2:
            return dates[0], dates[1]
        return None, None

    def run(self, employee_id: str, company_id: str, team_id: str, query: str):
        intent = self.classify_intent(query)

        if intent == "leave_request":
            leave_start, leave_end = self.extract_dates(query)
            if not leave_start:
                return {
                    "acceptance_score": 0.0,
                    "report": "Could not detect valid dates in your request."
                }

            # let the LLM prepare a report and a rating
            eval_prompt = f"""
            You are an HR assistant. Evaluate the following leave request:

            - Employee: {employee_id}
            - Company: {company_id}
            - Team: {team_id}
            - Leave period: {leave_start} → {leave_end}

            Return:
            1. A numeric acceptance_score between 0.0 and 1.0.
            2. A short report explaining the reasoning.
            """

            report = self.llm.predict(eval_prompt)

            # you can either parse the score from the LLM or keep it heuristic
            return {
                "acceptance_score": 0.8,   # simple placeholder score
                "report": report.strip()
            }

        else:  # chatbot mode
            answer = self.llm.predict(f"You are a PTO assistant. Answer clearly: {query}")
            return {
                "acceptance_score": None,
                "report": answer.strip()
            }