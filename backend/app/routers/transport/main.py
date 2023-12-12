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


@router.get("/get_modes_of_transport", response_model=List[schemas.Transport])
async def read_transportation_by_country(country_id: int, skip: int = 0,
                                         limit: int = 100,
                                         db: Session = Depends(get_db)):
    """Endpoint to read modes of transport based on country_id"""

    trans = crud.get_transports_by_country(db, country_id=country_id,
                                           skip=skip, limit=limit)
    return trans


@router.get("/transport/{transport_id}", response_model=schemas.Transport)
async def read_transport(transport_id: int, db: Session = Depends(get_db)):
    """Endpoint to read mode of transport based on its id"""

    db_trans = crud.get_transport(db, transport_id=transport_id)
    if db_trans is None:
        raise HTTPException(status_code=404, detail="Transport mode not found")
    return db_trans


@router.post("/create_transport/{country_id}",
             response_model=schemas.Transport)
async def create_transport_for_country(country_id: int,
                                       transport: schemas.TransportCreate,
                                       db: Session = Depends(get_db)):
    """Endpoint to create transport mode based on country_id"""

    return crud.create_transport(db=db, transport=transport,
                                 country_id=country_id)


@router.put("/update_transport/{transport_id}",
            response_model=schemas.Transport)
async def update_transport(transport_id: int,
                           transport_update: schemas.TransportBase,
                           db: Session = Depends(get_db)):
    """Endpoint to update mode of transport based on its id"""

    return crud.update_transport(db, transport_id, transport_update)


@router.delete("/delete_transport/{transport_id}", response_model=None)
async def delete_transport(transport_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete transport mode based on its id"""

    crud.delete_transport(db, transport_id)
    return {"message": "Transportation mode deleted successfully"}
