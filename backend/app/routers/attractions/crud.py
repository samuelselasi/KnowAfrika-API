#!/usr/bin/python3
"""Module that defines CRUD functions"""

from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session


def get_tour(db: Session, tour_id: int):
    """Function to read an attraction based on its id"""

    return db.query(models.Tour).filter(models.Tour.id == tour_id).first()


def get_tour_by_name(db: Session, tour_name: str):
    """Function to return a specific attraction based on its name"""

    return db.query(models.Tour).filter(
            models.Tour.name.ilike(f'%{tour_name}%')).first()


def get_tours_by_country(db: Session, country_id: int,
                         skip: int = 0, limit: int = 100):
    """Function to read attractions based on country"""

    return db.query(models.Tour).filter(models.Tour.country_id ==
                                        country_id).offset(
                                                skip).limit(limit).all()


def get_tours_by_country_and_province(db: Session,
                                      country_id: int,
                                      province_id: int,
                                      skip: int = 0,
                                      limit: int = 100):
    """Function to read attractions based on country and province"""

    return db.query(models.Tour).filter(models.Tour.country_id ==
                                        country_id,
                                        models.Tour.province_id ==
                                        province_id).offset(
                                                skip).limit(limit).all()


def get_tours_by_country_and_province_and_city(db: Session,
                                               country_id: int,
                                               province_id: int,
                                               city_id: int,
                                               skip: int = 0,
                                               limit: int = 100):
    """Function to read attractions based on country, province and city"""

    return db.query(models.Tour).filter(models.Tour.country_id ==
                                        country_id,
                                        models.Tour.province_id ==
                                        province_id,
                                        models.Tour.city_id ==
                                        city_id).offset(
                                                skip).limit(limit).all()


def create_tour(db: Session, tour: schemas.TourCreate,
                country_id: int, province_id: int, city_id: int):
    """Function to create a tour for country based on province & city"""

    db_tour = models.Tour(**tour.dict(), country_id=country_id,
                          province_id=province_id, city_id=city_id)
    db.add(db_tour)
    db.commit()
    db.refresh(db_tour)
    return db_tour


def update_tour(db: Session, tour_id: int, tour_update: schemas.TourBase):
    """Function to update an attraction based on its id"""

    db_tour = get_tour(db, tour_id=tour_id)
    if db_tour:
        for key, value in tour_update.dict().items():
            setattr(db_tour, key, value)
        db.commit()
        db.refresh(db_tour)
        return db_tour
    else:
        raise HTTPException(status_code=404, detail="Attraction not found")


def delete_tour(db: Session, tour_id: int):
    """Function to delete an attraction based on its id"""

    db_tour = get_tour(db, tour_id=tour_id)
    if db_tour:
        db.delete(db_tour)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Attraction not found")
