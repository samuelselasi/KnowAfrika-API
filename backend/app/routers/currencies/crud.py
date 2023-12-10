#!/usr/bin/python3
"""Module that defines CRUD functions"""

from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session


def get_currency(db: Session, currency_id: int):
    """Function to get currency based on its id"""

    return db.query(models.Currency).filter(models.Currency.id ==
                                            currency_id).first()


def get_currencies_by_country(db: Session, country_id: int, skip: int = 0,
                              limit: int = 100):
    """Function to get currency based on country id"""

    return db.query(models.Currency).filter(models.Currency.country_id ==
                                            country_id).offset(skip).limit(
                                                    limit).all()


def create_currency(db: Session, currency: schemas.CurrencyCreate,
                    country_id: int):
    """Function to create currency for a country"""

    db_currency = models.Currency(**currency.dict(), country_id=country_id)
    db.add(db_currency)
    db.commit()
    db.refresh(db_currency)
    return db_currency


def update_currency(db: Session, currency_id: int,
                    currency_update: schemas.CurrencyBase):
    """Function to update currency of a country based on its id"""

    db_currency = get_currency(db, currency_id=currency_id)
    if db_currency:
        for key, value in currency_update.dict().items():
            setattr(db_currency, key, value)
        db.commit()
        db.refresh(db_currency)
        return db_currency
    else:
        raise HTTPException(status_code=404, detail="Currency not found")


def delete_currency(db: Session, currency_id: int):
    """Funtion to delete currency based on its id"""

    db_currency = get_currency(db, currency_id=currency_id)
    if db_currency:
        db.delete(db_currency)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Currency not found")
