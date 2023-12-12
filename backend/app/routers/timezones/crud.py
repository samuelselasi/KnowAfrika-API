#!/usr/bin/python3
"""Module that defines CRUD functions"""

from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session


def get_timezone(db: Session, timezone_id: int):
    """Function to get timezone based on its id"""

    return db.query(models.Timezone).filter(models.Timezone.id ==
                                            timezone_id).first()


def get_timezones_by_country(db: Session, country_id: int, skip: int = 0,
                             limit: int = 100):
    """Function to get timezone based on country id"""

    return db.query(models.Timezone).filter(models.Timezone.country_id ==
                                            country_id).offset(skip).limit(
                                                    limit).all()


def create_timezone(db: Session, timezone: schemas.TimezoneCreate,
                    country_id: int):
    """Function to create timezone for a country"""

    db_timezone = models.Timezone(**timezone.dict(), country_id=country_id)
    db.add(db_timezone)
    db.commit()
    db.refresh(db_timezone)
    return db_timezone


def update_timezone(db: Session, timezone_id: int,
                    timezone_update: schemas.TimezoneBase):
    """Function to update timezone of a country based on its id"""

    db_timezone = get_timezone(db, timezone_id=timezone_id)
    if db_timezone:
        for key, value in timezone_update.dict().items():
            setattr(db_timezone, key, value)
        db.commit()
        db.refresh(db_timezone)
        return db_timezone
    else:
        raise HTTPException(status_code=404, detail="Timezone not found")


def delete_timezone(db: Session, timezone_id: int):
    """Funtion to delete timezone based on its id"""

    db_timezone = get_timezone(db, timezone_id=timezone_id)
    if db_timezone:
        db.delete(db_timezone)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Timezone not found")
