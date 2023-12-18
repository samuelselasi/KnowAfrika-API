#!/usr/bin/python3
"""Module that defines CRUD functions"""

from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session


def get_flag(db: Session, flag_id: int):
    """Function to get flag based on its id"""

    return db.query(models.Flag).filter(models.Flag.id == flag_id).first()


def get_flag_by_country(db: Session, country_id: int):
    """Function to get flag based on country id"""

    return db.query(models.Flag).filter(models.Flag.country_id ==
                                        country_id).first()


def get_flag_by_country_name(db: Session, country_name: str):
    """Function to get flag based on country name"""

    return db.query(models.Flag).filter(
            models.Flag.title.ilike(f'%{country_name}%')).first()


def create_flag(db: Session, flag: schemas.FlagCreate, country_id: int):
    """Function to create flag for a country"""

    db_flag = models.Flag(**flag.dict(), country_id=country_id)
    db.add(db_flag)
    db.commit()
    db.refresh(db_flag)
    return db_flag


def update_flag(db: Session, flag_id: int, flag_update: schemas.FlagBase):
    """Function to update flag of a country based on its id"""

    db_flag = get_flag(db, flag_id=flag_id)
    if db_flag:
        for key, value in flag_update.dict().items():
            setattr(db_flag, key, value)
        db.commit()
        db.refresh(db_flag)
        return db_flag
    else:
        raise HTTPException(status_code=404, detail="Flag not found")


def delete_flag(db: Session, flag_id: int):
    """Funtion to delete flag based on its id"""

    db_flag = get_flag(db, flag_id=flag_id)
    if db_flag:
        db.delete(db_flag)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Flag not found")
