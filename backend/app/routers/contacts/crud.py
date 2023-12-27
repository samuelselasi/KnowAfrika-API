#!/usr/bin/python3
"""Module that defines CRUD functions"""

from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_


def get_contact(db: Session, contact_id: int):
    """Function to get contact based on its id"""

    return db.query(models.Contact).filter(models.Contact.id ==
                                           contact_id).first()


def get_contacts_by_country(db: Session, country_id: int, skip: int = 0,
                            limit: int = 100):
    """Function to get contacts based on country id"""

    return db.query(models.Contact).filter(models.Contact.country_id ==
                                           country_id).offset(skip).limit(
                                                   limit).all()


def get_contact_by_country_and_name(db: Session, country_id: int,
                                    contact_name: str, skip: int = 0,
                                    limit: int = 100):
    """Function to get contacts based on country id and name"""

    return db.query(models.Contact).filter(and_(
        models.Contact.country_id == country_id,
        models.Contact.name.ilike(f'%{contact_name}%'))).first()


def get_contact_by_name(db: Session, contact_name: str):
    """Function to return a specific contact based on its name"""

    return db.query(models.Contact).filter(
            models.Contact.name.ilike(f'%{contact_name}%')).first()


def create_contact(db: Session, contact: schemas.ContactCreate,
                   country_id: int):
    """Function to create contact for a country"""

    db_contact = models.Contact(**contact.dict(), country_id=country_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int,
                   contact_update: schemas.ContactBase):
    """Function to update contact of a country based on its id"""

    db_contact = get_contact(db, contact_id=contact_id)
    if db_contact:
        for key, value in contact_update.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    else:
        raise HTTPException(status_code=404, detail="Contact not found")


def delete_contact(db: Session, contact_id: int):
    """Funtion to delete contact based on its id"""

    db_contact = get_contact(db, contact_id=contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Contact not found")
