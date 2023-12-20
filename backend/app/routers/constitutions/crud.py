#!/usr/bin/python3
"""Module that defines CRUD functions"""

from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session


def get_constitution(db: Session, constitution_id: int):
    """Function to get constitution based on its id"""

    return db.query(models.Constitution).filter(
            models.Constitution.id == constitution_id).first()


def get_constitution_by_country(db: Session, country_id: int):
    """Function to get constitution based on country id"""

    return db.query(models.Constitution).filter(
            models.Constitution.country_id == country_id).first()


def get_constitution_by_country_name(db: Session, country_name: str):
    """Function to get constitution based on country name"""

    return db.query(models.Constitution).filter(
            models.Constitution.title.ilike(f'%{country_name}%')).first()


def create_constitution(db: Session, constitution: schemas.ConstitutionCreate,
                        country_id: int):
    """Function to create constitution for a country"""

    db_constitution = models.Constitution(**constitution.dict(),
                                          country_id=country_id)
    db.add(db_constitution)
    db.commit()
    db.refresh(db_constitution)
    return db_constitution


def update_constitution(db: Session, constitution_id: int,
                        constitution_update: schemas.ConstitutionBase):
    """Function to update constitution of a country based on its id"""

    db_constitution = get_constitution(db, constitution_id=constitution_id)
    if db_constitution:
        for key, value in constitution_update.dict().items():
            setattr(db_constitution, key, value)
        db.commit()
        db.refresh(db_constitution)
        return db_constitution
    else:
        raise HTTPException(status_code=404, detail="Constitution not found")


def delete_constitution(db: Session, constitution_id: int):
    """Funtion to delete constitution based on its id"""

    db_constitution = get_constitution(db, constitution_id=constitution_id)
    if db_constitution:
        db.delete(db_constitution)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Constitution not found")
