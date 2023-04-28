""" Module for crud for Companies """
from typing import Optional

from sqlalchemy.orm import Session

from app.dependency import get_db
from app.model.company import Company
from app.schema.company import CompanyCreate, CompanyInfoBase


def get_company_by_name(name: Optional[str]) -> Optional[Company]:
    """ return Company from email """
    db:Session = next(get_db())
    return db.query(Company).filter(Company.name == name).first()

def get_company_by_id(id_company: str) -> Optional[Company]:
    """ Return the Company from id_company """
    db:Session = next(get_db())
    return db.query(Company).filter(Company.id_company == id_company).first()

def get_company_by_user_id(user_id: str) -> Optional[Company]:
    """ Return the Company from user_id """
    db:Session = next(get_db())
    return db.query(Company).filter(Company.id_user == user_id).first()

def create_company(company: CompanyCreate) -> Optional[Company]:
    """ Creation a user, in input the schema of user create and return the user"""
    db:Session = next(get_db())
    db_company = Company(name=company.name, id_user=company.id_user, id_instagram=company.id_instagram, website=company.website, description=company.description)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(company: Company, company_edit: CompanyInfoBase) -> Optional[Company]:
    """ Permit to edit info inside company model """
    db:Session = next(get_db())
    company_data = company_edit.dict(exclude_unset=True)
    for key, value in company_data.items():
        setattr(company, key, value)
    db.merge(company)
    db.commit()
    return company

def delete_company(company: Company) -> Optional[Company]:
    """" Permit to delete a company """
    db:Session = next(get_db())
    db.delete(company)
    db.commit()
    return {"ok": True}
