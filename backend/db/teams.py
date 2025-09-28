from .mongo import db

def get_team_notices(team_id: str) -> list:
    """
    Get team-level PTO blackout notices from the teams collection.
    """
    team = db.teams.find_one({"_id": team_id}, {"notices": 1})
    return team.get("notices", []) if team else []
