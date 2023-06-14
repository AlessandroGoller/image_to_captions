""" Module for crud for Companies """
from typing import Optional

from sqlalchemy.orm import Session

from app.crud.instagram import delete_all_instagram
from app.dependency import get_db
from app.model.company import Company
from app.schema.company import CompanyCreate, CompanyInfoBase
from app.utils.logger import configure_logger

logger = configure_logger()

def get_company_by_name(name: str) -> Optional[Company]:
    """return Company from email"""
    db: Session = next(get_db())
    return db.query(Company).filter(Company.name == name).first()  # type: ignore

def get_company_by_id(id_company: int) -> Optional[Company]:
    """Return the Company from id_company"""
    db: Session = next(get_db())
    return db.query(Company).filter(Company.id_company == id_company).first()  # type: ignore

def get_company_by_user_id(user_id: int) -> Optional[Company]:
    """Return the Company from user_id"""
    db: Session = next(get_db())
    return db.query(Company).filter(Company.id_user == user_id).first()  # type: ignore

def create_company(company: CompanyCreate) -> Optional[Company]:
    """Creation a user, in input the schema of user create and return the user"""
    db: Session = next(get_db())
    db_company = Company(
        name=company.name,
        id_user=company.id_user,
        url_instagram=company.url_instagram,
        website=company.website,
        description=company.description,
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def remove_account_ig(id_company: int)->Optional[Company]:
    """ Permit to remove the instagram account """
    logger.info("Updating Instagram account")
    delete_all_instagram(id_company=id_company)
    db: Session = next(get_db())
    company = get_company_by_id(id_company=id_company)
    company.url_instagram = "" # type: ignore
    db.merge(company)
    db.commit()
    return company

def update_account_ig(company: Company, ig_account:str)->Optional[Company]:
    """ Permit to change the instagram account """
    db: Session = next(get_db())
    company.url_instagram = ig_account
    logger.info("Updating Instagram account")
    delete_all_instagram(id_company=company.id_company)
    db.merge(company)
    db.commit()
    return company

def add_profile_pic(company: Company, url_pic:str)-> None:
    """ Add or edit a profile url pic """
    db: Session = next(get_db())
    company.profile_pic_url = url_pic
    logger.info("Updating Profile pic url")
    db.merge(company)
    db.commit()

def update_company(
    company: Company, company_edit: CompanyInfoBase
) -> Optional[Company]:
    """Permit to edit info inside company model"""
    db: Session = next(get_db())
    company_data = company_edit.dict(exclude_unset=True)
    for key, value in company_data.items():
        setattr(company, key, value)
    db.merge(company)
    db.commit()
    return company


def delete_company(company: Company) -> dict[str, bool]:
    """ " Permit to delete a company"""
    logger.info("Delete Company")
    db: Session = next(get_db())
    db.delete(company)
    db.commit()
    return {"ok": True}
