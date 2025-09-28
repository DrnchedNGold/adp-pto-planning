from datetime import datetime
from dateutil import parser
from .policy_agent import PolicyAgent
from .coverage_agent import CoverageAgent
from .config import get_llm
import json
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain


class OrchestratorAgent:
    def __init__(self):
        self.policy_agent = PolicyAgent()
        self.coverage_agent = CoverageAgent()
        self.llm = get_llm()

        # simple classification chain (leave_request vs chatbot)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Classify user query into either 'leave_request' or 'chatbot'."),
            ("user", "{query}")
        ])
        self.classifier = LLMChain(llm=self.llm, prompt=prompt)

    def classify_intent(self, query: str) -> str:
        result = self.classifier.run(query)
        if "leave_request" in result.lower():
            return "leave_request"
        return "chatbot"

    def extract_dates(self, query: str):
        # naive date extraction using dateutil
        # you can improve this with a dedicated tool later
        words = query.split()
        dates = []
        for word in words:
            try:
                parsed = parser.parse(word, fuzzy=True, dayfirst=False)
                dates.append(parsed)
            except Exception:
                continue
        if len(dates) == 1:
            return dates[0].strftime("%Y-%m-%d"), dates[0].strftime("%Y-%m-%d")
        elif len(dates) >= 2:
            return dates[0].strftime("%Y-%m-%d"), dates[1].strftime("%Y-%m-%d")
        else:
            return None, None

    def run(self, employee_id: str, company_id: str, team_id: str, query: str):
        intent = self.classify_intent(query)

        if intent == "leave_request":
            leave_start, leave_end = self.extract_dates(query)
            if not leave_start:
                return {
                    "error": "Could not detect valid dates in your request.",
                    "intent": intent
                }

            # Call sub-agents
            policy_result_raw = self.policy_agent.run(
                employee_id, company_id, team_id, leave_start, leave_end
            )
            coverage_result_raw = self.coverage_agent.run(
                employee_id, team_id, leave_start, leave_end
            )

            # Parse outputs safely
            try:
                policy_result = json.loads(policy_result_raw)
            except Exception:
                policy_result = {"policy_score": 0, "notes": policy_result_raw}

            try:
                coverage_result = json.loads(coverage_result_raw)
            except Exception:
                coverage_result = {"coverage_score": 0, "uncovered_tasks": [coverage_result_raw]}

            # Merge scores
            policy_score = policy_result.get("policy_score", 0)
            coverage_score = coverage_result.get("coverage_score", 0)
            combined_score = (policy_score + coverage_score) / 2

            return {
                "intent": intent,
                "acceptance_score": combined_score,
                "policy_notes": policy_result.get("notes"),
                "coverage_uncovered": coverage_result.get("uncovered_tasks"),
            }

        else:  # chatbot query
            chatbot_prompt = f"""
            You are a friendly assistant that answers PTO-related questions.
            If the user is indirectly asking about leave rules, base your answer
            on company PTO policies and general HR knowledge.
            
            User query: {query}
            """
            answer = self.llm.predict(chatbot_prompt)
            return {
                "intent": intent,
                "answer": answer
            }
        
def test_orchestrator():
    orch = OrchestratorAgent()

    # Case 1: Leave request with dates
    query1 = "Can I take leave from June 10 to June 14?"
    result1 = orch.run(employee_id="68d8c0500194311185f8d5d9", company_id="68d8c04f0194311185f8d5c4", team_id="T68d8c0500194311185f8d5d8", query=query1)
    print("\n=== Test 1: Leave Request ===")
    print(result1)

    # # Case 2: General chatbot query
    # query2 = "How many PTO days do I get every year?"
    # result2 = orch.run(employee_id="E123", company_id="C456", team_id="T789", query=query2)
    # print("\n=== Test 2: Chatbot ===")
    # print(result2)

    # # Case 3: Invalid leave request (no dates)
    # query3 = "Can I go on vacation soon?"
    # result3 = orch.run(employee_id="E123", company_id="C456", team_id="T789", query=query3)
    # print("\n=== Test 3: Missing Dates ===")
    # print(result3)

if __name__ == "__main__":
    test_orchestrator()