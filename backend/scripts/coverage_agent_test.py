from agents.coverage_agent import CoverageAgent

if __name__ == "__main__":
    test_employee_id = "68d8c0500194311185f8d5d9"
    test_team_id = "68d8c0500194311185f8d5d8"
    test_leave_start = "2025-07-08T04:57:53.499+00:00"
    test_leave_end = "2025-07-15T04:57:53.499+00:00"

    agent = CoverageAgent()
    agent.run(test_employee_id, test_team_id, test_leave_start, test_leave_end)
