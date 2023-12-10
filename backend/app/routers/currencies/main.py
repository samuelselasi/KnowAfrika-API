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


@router.get("/get_currencies", response_model=List[schemas.Currency])
async def read_currencies_by_country(country_id: int,
                                     skip: int = 0,
                                     limit: int = 100,
                                     db: Session = Depends(get_db)):
    """Endpoint to read currencies based on country_id"""

    currencies = crud.get_currencies_by_country(db,
                                                country_id=country_id,
                                                skip=skip,
                                                limit=limit)
    return currencies


@router.get("/currency/{currency_id}", response_model=schemas.Currency)
async def read_currency(currency_id: int, db: Session = Depends(get_db)):
    """Endpoint to read currency based on its id"""

    db_currency = crud.get_currency(db, currency_id=currency_id)
    if db_currency is None:
        raise HTTPException(status_code=404, detail="Currency not found")
    return db_currency


@router.post("/create_currency/{country_id}", response_model=schemas.Currency)
async def create_currency_for_country(country_id: int,
                                      currency: schemas.CurrencyCreate,
                                      db: Session = Depends(get_db)):
    """Endpoint to create currency based on country_id"""

    return crud.create_currency(db=db,
                                currency=currency,
                                country_id=country_id)


@router.put("/update_currency/{currency_id}", response_model=schemas.Currency)
async def update_currency(currency_id: int,
                          currency_update: schemas.CurrencyBase,
                          db: Session = Depends(get_db)):
    """Endpoint to update currency based on its id"""

    return crud.update_currency(db, currency_id, currency_update)


@router.delete("/delete_currency/{currency_id}", response_model=None)
async def delete_currency(currency_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete currency based on its id"""

    crud.delete_currency(db, currency_id)
    return {"message": "Currency deleted successfully"}
