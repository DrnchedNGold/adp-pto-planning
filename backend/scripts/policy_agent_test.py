from agents.policy_agent import PolicyAgent

if __name__ == "__main__":
    agent = PolicyAgent()
    result = agent.run(
        employee_id="68d8b38f3eb872dbb05fd4a3",
        company_id="68d8b38f3eb872dbb05fd48e",
        team_id="68d8b38f3eb872dbb05fd49c",
        leave_start="2025-12-24",
        leave_end="2025-12-28"
    )
    print("Policy Agent Result:\n", result)
