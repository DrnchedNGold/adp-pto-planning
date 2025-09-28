from .mongo import db

def get_company_holidays(company_id: str) -> list:
    """
    Get company-wide holidays from the companies collection.
    """
    company = db.companies.find_one({"_id": company_id}, {"holidays": 1})
    return company.get("holidays", []) if company else []
