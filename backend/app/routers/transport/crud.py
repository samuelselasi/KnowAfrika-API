#!/usr/bin/python3
"""Module that defines CRUD functions"""

from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session


def get_transport(db: Session, transport_id: int):
    """Function to get mode of transport based on its id"""

    return db.query(models.Transport).filter(models.Transport.id ==
                                             transport_id).first()


def get_transports_by_country(db: Session, country_id: int, skip: int = 0,
                              limit: int = 100):
    """Function to get modes of transport based on country id"""

    return db.query(models.Transport).filter(models.Transport.country_id ==
                                             country_id).offset(skip).limit(
                                                     limit).all()


def create_transport(db: Session, transport: schemas.TransportCreate,
                     country_id: int):
    """Function to create mode of transport for a country"""

    db_transport = models.Transport(**transport.dict(), country_id=country_id)
    db.add(db_transport)
    db.commit()
    db.refresh(db_transport)
    return db_transport


def update_transport(db: Session, transport_id: int,
                     transport_update: schemas.TransportBase):
    """Function to update mode of transport based on its id"""

    db_transport = get_transport(db, transport_id=transport_id)
    if db_transport:
        for key, value in transport_update.dict().items():
            setattr(db_transport, key, value)
        db.commit()
        db.refresh(db_transport)
        return db_transport
    else:
        raise HTTPException(status_code=404,
                            detail="Transport mode not found")


def delete_transport(db: Session, transport_id: int):
    """Funtion to delete mode of transport based on its id"""

    db_transport = get_transport(db, transport_id=transport_id)
    if db_transport:
        db.delete(db_transport)
        db.commit()
    else:
        raise HTTPException(status_code=404,
                            detail="Transport mode not found")
