from .mongo import db
from bson import ObjectId
from datetime import datetime

def get_team_members_with_roles(team_id: str):
    """Return team members with their roles."""
    query_id = ObjectId(team_id) if ObjectId.is_valid(team_id) else team_id
    members = list(db.employees.find({"team_id": query_id}, {"name": 1, "role": 1}))
    return members


def get_overlapping_leaves(team_id: str, leave_start: str, leave_end: str):
    """Return leaves that overlap with requested period for the team."""
    query_id = ObjectId(team_id) if ObjectId.is_valid(team_id) else team_id
    start = datetime.fromisoformat(leave_start)
    end = datetime.fromisoformat(leave_end)

    leaves = list(db.leave_requests.find({
        "team_id": query_id,
        "status": {"$in": ["approved", "pending"]},
        "start_date": {"$lte": end},
        "end_date": {"$gte": start}
    }, {"employee_id": 1, "start_date": 1, "end_date": 1}))
    return leaves

if __name__ == "__main__":
    team_id = "68d8c0500194311185f8d5cf"
    test_leave_start = "2025-12-03T04:57:53.499+00:00"
    test_leave_end = "2025-12-07T04:57:53.499+00:00"
    leaves = get_overlapping_leaves(team_id, test_leave_start, test_leave_end)
    print(leaves)