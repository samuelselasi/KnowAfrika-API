#!/usr/bin/python3
"""Module that defines CRUD functions"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas


def get_city(db: Session, city_id: int):
    """Function that prints a city by id"""

    return db.query(models.City).filter(models.City.id ==
                                        city_id).first()


def get_cities_by_country(db: Session, country_id: int,
                          skip: int = 0, limit: int = 100):
    """Function that prints cities by country_id"""

    return db.query(models.City).filter(models.City.country_id ==
                                        country_id).offset(skip).limit(
                                                limit).all()


def get_cities_by_country_and_province(db: Session, country_id: int,
                                       province_id: int, skip: int = 0,
                                       limit: int = 100):
    """Function that prints cities by country_id and province_id"""

    return db.query(models.City).filter(models.City.country_id ==
                                        country_id,
                                        models.City.province_id ==
                                        province_id).offset(skip).limit(
                                                limit).all()


def get_cities_by_province(db: Session, province_id: int, skip: int = 0,
                           limit: int = 100):
    """Function that prints cities by province_id"""

    return db.query(models.City).filter(models.City.province_id ==
                                        province_id).offset(skip).limit(
                                                limit).all()


def get_city_by_name(db: Session, city_name: str):
    """Function to return a specific city based on its name"""

    return db.query(models.City).filter(
            models.City.name.ilike(f'%{city_name}%')).first()


def create_city(db: Session, city: schemas.CityCreate,
                country_id: int, province_id: int):
    """Function that creates a city based on a country and province"""

    db_city = models.City(**city.dict(), country_id=country_id,
                          province_id=province_id)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def update_city(db: Session, city_id: int,
                city_update: schemas.CityBase):
    """Function that updates a city based on its id"""

    db_city = get_city(db, city_id=city_id)
    if db_city:
        for key, value in city_update.dict().items():
            setattr(db_city, key, value)
        db.commit()
        db.refresh(db_city)
        return db_city
    else:
        raise HTTPException(status_code=404, detail="City not found")


def delete_city(db: Session, city_id: int):
    """Function that deletes a city based on it id"""

    db_city = get_city(db, city_id=city_id)
    if db_city:
        db.delete(db_city)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="City not found")
