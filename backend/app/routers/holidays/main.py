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


@router.get("/get_holidays", response_model=List[schemas.Holiday])
async def read_holidays_by_country(country_id: int,
                                   skip: int = 0,
                                   limit: int = 100,
                                   db: Session = Depends(get_db)):
    """Endpoint to read holidays based on country_id"""

    holidays = crud.get_holidays_by_country(db,
                                            country_id=country_id,
                                            skip=skip,
                                            limit=limit)
    return holidays


@router.get("/holiday/{holiday_id}", response_model=schemas.Holiday)
async def read_holiday(holiday_id: int, db: Session = Depends(get_db)):
    """Endpoint to read holiday based on its id"""

    db_holiday = crud.get_holiday(db, holiday_id=holiday_id)
    if db_holiday is None:
        raise HTTPException(status_code=404, detail="Holiday not found")
    return db_holiday


@router.get("/get_holiday_by_name", response_model=schemas.Holiday)
async def read_holiday_by_name(
        holiday_name: str, db: Session = Depends(get_db)):
    """Endpoint to read holiday based on its name"""

    db_holiday = crud.get_holiday_by_name(db, holiday_name=holiday_name)
    if db_holiday is None:
        raise HTTPException(status_code=404, detail="Holiday not found")
    return db_holiday


@router.post("/create_holiday/{country_id}", response_model=schemas.Holiday)
async def create_holiday_for_country(country_id: int,
                                     holiday: schemas.HolidayCreate,
                                     db: Session = Depends(get_db)):
    """Endpoint to create holiday based on country_id"""

    return crud.create_holiday(db=db,
                               holiday=holiday,
                               country_id=country_id)


@router.put("/update_holiday/{holiday_id}", response_model=schemas.Holiday)
async def update_holiday(holiday_id: int,
                         holiday_update: schemas.HolidayBase,
                         db: Session = Depends(get_db)):
    """Endpoint to update holiday based on its id"""

    return crud.update_holiday(db, holiday_id, holiday_update)


@router.delete("/delete_holiday/{holiday_id}", response_model=None)
async def delete_holiday(holiday_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete holiday based on its id"""

    crud.delete_holiday(db, holiday_id)
    return {"message": "Holiday deleted successfully"}
