#!/usr/bin/python3
"""Module that defines endpoints"""

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


@router.get("/get_timezones", response_model=List[schemas.Timezone])
async def read_timezone_by_country(country_id: int, skip: int = 0,
                                   limit: int = 100,
                                   db: Session = Depends(get_db)):
    """Endpoint to read tiezone based on country_id"""

    timezone = crud.get_timezones_by_country(db,
                                             country_id=country_id,
                                             skip=skip,
                                             limit=limit)
    return timezone


@router.get("/timezone/{timezone_id}", response_model=schemas.Timezone)
async def read_timezone(timezone_id: int, db: Session = Depends(get_db)):
    """Endpoint to read timezone based on its id"""

    db_timezone = crud.get_timezone(db, timezone_id=timezone_id)
    if db_timezone is None:
        raise HTTPException(status_code=404, detail="Timezone not found")
    return db_timezone


@router.post("/create_timezone/{country_id}", response_model=schemas.Timezone)
async def create_timezone_for_country(country_id: int,
                                      timezone: schemas.TimezoneCreate,
                                      db: Session = Depends(get_db)):
    """Endpoint to create timezone based on country_id"""

    return crud.create_timezone(db=db, timezone=timezone,
                                country_id=country_id)


@router.put("/update_timezone/{timezone_id}", response_model=schemas.Timezone)
async def update_timezone(timezone_id: int,
                          timezone_update: schemas.TimezoneBase,
                          db: Session = Depends(get_db)):
    """Endpoint to update timezone based on its id"""

    return crud.update_timezone(db, timezone_id, timezone_update)


@router.delete("/delete_timezone/{timezone_id}", response_model=None)
async def delete_timezone(timezone_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete timezone based on its id"""

    crud.delete_timezone(db, timezone_id)
    return {"message": "Timezone deleted successfully"}
