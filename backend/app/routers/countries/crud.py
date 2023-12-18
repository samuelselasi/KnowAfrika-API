#!/usr/bin/python3
"""Module that defines CRUD functions"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas


def get_countries(db: Session, skip: int = 0, limit: int = 100):
    """Function to return countries"""

    return db.query(models.Country).offset(skip).limit(limit).all()


def get_country(db: Session, country_id: int):
    """Function to return a specific country based on its id"""

    return db.query(models.Country).filter(models.Country.id ==
                                           country_id).first()

def get_country_by_name(db: Session, country_name: str):
    """Function to return a specific country based on its name"""

    return db.query(models.Country).filter(
            models.Country.name.ilike(f'%{country_name}%')).first()


def create_region_country(db: Session, country: schemas.CountryCreate,
                          region_id: int):
    """Function to create a country in a specific region"""

    db_country = models.Country(**country.dict(), region_id=region_id)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country


def update_country(db: Session, country_id: int,
                   country_update: schemas.CountryBase):
    """Function to update a country based on its id"""

    db_country = get_country(db, country_id=country_id)
    if db_country:
        for key, value in country_update.dict().items():
            setattr(db_country, key, value)
        db.commit()
        db.refresh(db_country)
        return db_country
    else:
        raise HTTPException(status_code=404, detail="Country not found")


def delete_country(db: Session, country_id: int):
    """Function to delete a country based on its id"""

    db_country = get_country(db, country_id=country_id)
    if db_country:
        db.delete(db_country)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Country not found")
