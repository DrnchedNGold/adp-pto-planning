from .mongo import db
from bson import ObjectId

def get_company_holidays(company_id: str) -> list:
    """
    Get company-wide holidays from the companies collection.
    Accepts ObjectId or string (with or without 'company_id:' prefix).
    """
    # sanitize input
    query_id = ObjectId(company_id) if ObjectId.is_valid(company_id) else company_id
    company = db.companies.find_one({"_id": query_id}, {"holidays": 1})
    return company.get("holidays", []) if company else []
