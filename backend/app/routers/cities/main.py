#!/usr/bin/python3
"""Module that defines endpoints for cities"""

from typing import List
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi import Depends, HTTPException, APIRouter

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/get_city/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: Session = Depends(get_db)):
    """Endpoint to get a city based on its id"""

    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.get("/get_cities_country", response_model=List[schemas.City])
async def read_cities_by_country(country_id: int, skip: int = 0,
                                 limit: int = 100,
                                 db: Session = Depends(get_db)):
    """Endpoint to get cities based on country id"""

    cities = crud.get_cities_by_country(db, country_id=country_id,
                                        skip=skip, limit=limit)
    return cities


@router.get("/get_cities_province", response_model=List[schemas.City])
async def read_cities_by_province(province_id: int,
                                  skip: int = 0, limit: int = 100,
                                  db: Session = Depends(get_db)):
    """Endpoint to get cities based on country id & province id"""

    cities = crud.get_cities_by_province(db,
                                         province_id=province_id,
                                         skip=skip, limit=limit)
    return cities


@router.get("/get_cities_country_province", response_model=List[schemas.City])
async def read_cities_by_country_and_province(country_id: int,
                                              province_id: int,
                                              skip: int = 0, limit: int = 100,
                                              db: Session = Depends(get_db)):
    """Endpoint to get cities based on country id & province id"""

    cities = crud.get_cities_by_country_and_province(db,
                                                     country_id=country_id,
                                                     province_id=province_id,
                                                     skip=skip, limit=limit)
    return cities


@router.get("/get_city_by_name", response_model=schemas.City)
async def read_city_by_name(city_name: str, db: Session = Depends(get_db)):
    """Endpoint to read city based on its name"""

    db_city = crud.get_city_by_name(db, city_name=city_name)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.post("/create_city/{country_id}/{province_id}",
             response_model=schemas.City)
async def create_city_for_country_and_province(country_id: int,
                                               province_id: int,
                                               city: schemas.CityCreate,
                                               db: Session = Depends(get_db)):
    """Endpoint to create a city based on country_id and province_id"""

    return crud.create_city(db=db, city=city, country_id=country_id,
                            province_id=province_id)


@router.put("/update_city/{city_id}", response_model=schemas.City)
async def update_city(city_id: int, city_update: schemas.CityBase,
                      db: Session = Depends(get_db)):
    """Endpoint to update a city based on its id"""

    return crud.update_city(db, city_id, city_update)


@router.delete("/delete_city/{city_id}", response_model=None)
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete a city based on its id"""

    crud.delete_city(db, city_id)
    return {"message": "City deleted successfully"}
