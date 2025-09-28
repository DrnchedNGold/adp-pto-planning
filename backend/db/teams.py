from .mongo import db
from bson import ObjectId

def get_team_notices(team_id: str) -> list:
    """
    Get team-level PTO blackout notices from the teams collection.
    Accepts ObjectId or string (with or without 'team_id:' prefix).
    """
    query_id = ObjectId(team_id) if ObjectId.is_valid(team_id) else team_id
    team = db.teams.find_one({"_id": query_id}, {"notices": 1})
    return team.get("notices", []) if team else []

if __name__ == "__main__":
    test_employee_id = "68d8b38f3eb872dbb05fd49c"
    notices = get_team_notices(test_employee_id)
    print(notices)