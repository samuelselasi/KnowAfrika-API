#!/usr/bin/python3
"""Module that defines CRUD functions"""

from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session


def get_holiday(db: Session, holiday_id: int):
    """Function to get holiday based on its id"""

    return db.query(models.Holiday).filter(models.Holiday.id ==
                                           holiday_id).first()


def get_holidays_by_country(db: Session, country_id: int, skip: int = 0,
                            limit: int = 100):
    """Function to get holidays based on country id"""

    return db.query(models.Holiday).filter(models.Holiday.country_id ==
                                           country_id).offset(skip).limit(
                                                   limit).all()


def get_holiday_by_name(db: Session, holiday_name: str):
    """Function to return a specific holiday based on its name"""

    return db.query(models.Holiday).filter(
            models.Holiday.name.ilike(f'%{holiday_name}%')).first()


def create_holiday(db: Session, holiday: schemas.HolidayCreate,
                   country_id: int):
    """Function to create holiday for a country"""

    db_holiday = models.Holiday(**holiday.dict(), country_id=country_id)
    db.add(db_holiday)
    db.commit()
    db.refresh(db_holiday)
    return db_holiday


def update_holiday(db: Session, holiday_id: int,
                   holiday_update: schemas.HolidayBase):
    """Function to update holiday of a country based on its id"""

    db_holiday = get_holiday(db, holiday_id=holiday_id)
    if db_holiday:
        for key, value in holiday_update.dict().items():
            setattr(db_holiday, key, value)
        db.commit()
        db.refresh(db_holiday)
        return db_holiday
    else:
        raise HTTPException(status_code=404, detail="Holiday not found")


def delete_holiday(db: Session, holiday_id: int):
    """Funtion to delete holiday based on its id"""

    db_holiday = get_holiday(db, holiday_id=holiday_id)
    if db_holiday:
        db.delete(db_holiday)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Holiday not found")
