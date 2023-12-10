#!/usr/bin/python3
"""Module that defines CRUD functions"""

from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session


def get_province(db: Session, province_id: int):
    """Function to get province based on its id"""

    return db.query(models.Province).filter(models.Province.id ==
                                            province_id).first()


def get_provinces_by_country(db: Session, country_id: int, skip: int = 0,
                             limit: int = 100):
    """Function to get province based on country id"""

    return db.query(models.Province).filter(models.Province.country_id ==
                                            country_id).offset(skip).limit(
                                                    limit).all()


def create_province(db: Session, province: schemas.ProvinceCreate,
                    country_id: int):
    """Function to create province for a country"""

    db_province = models.Province(**province.dict(), country_id=country_id)
    db.add(db_province)
    db.commit()
    db.refresh(db_province)
    return db_province


def update_province(db: Session, province_id: int,
                    province_update: schemas.ProvinceBase):
    """Function to update province of a country based on its id"""

    db_province = get_province(db, province_id=province_id)
    if db_province:
        for key, value in province_update.dict().items():
            setattr(db_province, key, value)
        db.commit()
        db.refresh(db_province)
        return db_province
    else:
        raise HTTPException(status_code=404, detail="Province not found")


def delete_province(db: Session, province_id: int):
    """Funtion to delete province based on its id"""

    db_province = get_province(db, province_id=province_id)
    if db_province:
        db.delete(db_province)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Province not found")
