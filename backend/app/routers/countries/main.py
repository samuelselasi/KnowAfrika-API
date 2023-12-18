#!/usr/bin/python3
"""Module that defines endpoints for countries"""

from typing import List
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi import Depends, APIRouter, HTTPException

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/get_countries", response_model=List[schemas.Country])
async def read_countries(skip: int = 0,
                         limit: int = 100,
                         db: Session = Depends(get_db)):
    """Endpoint to read all countries"""

    countries = crud.get_countries(db, skip=skip, limit=limit)
    return countries


@router.get("/get_country/{country_id}", response_model=schemas.Country)
async def read_country(country_id: int, db: Session = Depends(get_db)):
    """Endpoint to read country based on its id"""

    db_country = crud.get_country(db, country_id=country_id)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country


@router.get("/get_country_by_name", response_model=schemas.Country)
async def read_country_by_name(country_name: str, db: Session = Depends(get_db)):
    """Endpoint to read country based on its name"""

    db_country = crud.get_country_by_name(db, country_name=country_name)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country


@router.post("/create_country/{region_id}", response_model=schemas.Country)
async def create_country_for_region(region_id: int,
                                    country: schemas.CountryCreate,
                                    db: Session = Depends(get_db)):
    """Endpoint to create a country based on region_id"""

    return crud.create_region_country(db=db,
                                      country=country,
                                      region_id=region_id)


@router.put("/update_country/{country_id}", response_model=schemas.Country)
async def update_country(country_id: int,
                         country_update: schemas.CountryBase,
                         db: Session = Depends(get_db)):
    """Endpoint to update a country based on its id"""

    return crud.update_country(db, country_id, country_update)


@router.delete("/delete_country/{country_id}", response_model=None)
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete a country based on its id"""

    crud.delete_country(db, country_id)
    return {"message": "Country deleted successfully"}
