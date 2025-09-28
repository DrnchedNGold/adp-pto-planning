import random
from datetime import datetime, timedelta
from faker import Faker
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

try:
    client = MongoClient(os.getenv("MONGO_DB"), server_api=ServerApi('1'))
    client.admin.command("ping")
    db = client["Eirene"]
except Exception as e:
    print("Failed to connect to MongoDB:", e)
    exit()

fake = Faker()

db.companies.drop()
db.managers.drop()
db.employees.drop()
db.teams.drop()
db.leave_requests.drop()
db.company_policies.drop()

company = {
    "name": "Eirene",
    "domain": "eirene.com"
}
company_id = db.companies.insert_one(company).inserted_id

managers = []
for i in range(10):
    manager = {
        "company_id": company_id,
        "name": fake.name(),
        "email": fake.email()
    }
    managers.append(manager)
manager_ids = db.managers.insert_many(managers).inserted_ids

notices_pool = [
    "No PTO allowed during product launch week",
    "Team coverage required during Q4 audits",
    "Blackout: Jan 1 - Jan 5",
    "Blackout: End of fiscal year",
    "No leave during client onboarding week",
    "Critical sprint — no PTO this week",
    "Holiday freeze — support team coverage only"
]

teams = []
for i in range(10):
    team = {
        "company_id": company_id,
        "name": f"{fake.word().capitalize()} Team",
        "manager_id": manager_ids[i],
        "members": [],
        "notices": random.sample(notices_pool, k=random.randint(1, 2))
    }
    teams.append(team)
team_ids = db.teams.insert_many(teams).inserted_ids

roles = [
    "Software Engineer",
    "Data Scientist",
    "Product Manager",
    "QA Engineer",
    "DevOps Engineer",
    "Business Analyst",
    "UX Designer",
    "Frontend Developer",
    "Backend Developer",
    "Database Administrator"
]

employees = []
for i in range(50):
    team_idx = random.randint(0, 9)
    employee = {
        "company_id": company_id,
        "team_id": team_ids[team_idx],
        "name": fake.name(),
        "email": fake.email(),
        "manager_id": manager_ids[team_idx],
        "role": random.choice(roles),
        "leave_balance": random.randint(5, 25)
    }
    employees.append(employee)
employee_ids = db.employees.insert_many(employees).inserted_ids

for emp in employees:
    db.teams.update_one(
        {"_id": emp["team_id"]},
        {"$push": {"members": emp["_id"]}}
    )

policy = {
    "company_id": company_id,
    "rules": {
        "max_leave_days": 90,
        "carry_over_days": 5
    },
    "holidays": ["2025-12-25"]
}
db.company_policies.insert_one(policy)

statuses = ["pending", "approved", "rejected"]
leave_requests = []

all_employees = list(db.employees.find({}))

for _ in range(100):
    emp = random.choice(all_employees)
    start_date = datetime.utcnow() + timedelta(days=random.randint(-90, 90))
    end_date = start_date + timedelta(days=random.randint(1, 7))
    status = random.choice(statuses)
    leave_request = {
        "company_id": company_id,
        "employee_id": emp["_id"],
        "team_id": emp["team_id"],
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "days_requested": (end_date - start_date).days + 1,
        "reason": fake.sentence(),
        "status": status,
        "submitted_at": datetime.utcnow().isoformat(),
        "decision": {}
    }
    if status != "pending":
        leave_request["decision"] = {
            "manager_id": emp["manager_id"],  
            "date": datetime.utcnow().isoformat(),
            "action": status,
            "note": fake.sentence()
        }
    leave_requests.append(leave_request)

db.leave_requests.insert_many(leave_requests)

print("Database seeded successfully!")
