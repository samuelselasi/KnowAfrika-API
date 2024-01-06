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


@router.get("/get_contacts/{country_id}",
            response_model=List[schemas.Contact])
async def read_contacts_by_country(country_id: int, skip: int = 0,
                                   limit: int = 100,
                                   db: Session = Depends(get_db)):
    """Endpoint to read emergency contact based on country_id"""

    contacts = crud.get_contacts_by_country(db,
                                            country_id=country_id,
                                            skip=skip,
                                            limit=limit)
    return contacts


@router.get("/get_contacts", response_model=schemas.Contact)
async def read_contacts_by_country_and_name(country_id: int,
                                            contact_name: str,
                                            db: Session = Depends(get_db)):
    """Endpoint to read emergency contact based on country_id and name"""

    contacts = crud.get_contact_by_country_and_name(db,
                                                    country_id=country_id,
                                                    contact_name=contact_name)
    return contacts


@router.get("/contact/{contact_id}", response_model=schemas.Contact)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    """Endpoint to read emergency contact based on its id"""

    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.get("/get_contact_by_name", response_model=schemas.Contact)
async def read_contact_by_name(
        contact_name: str, db: Session = Depends(get_db)):
    """Endpoint to read emergency contact based on its name"""

    db_contact = crud.get_contact_by_name(db, contact_name=contact_name)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.post("/create_contact/{country_id}", response_model=schemas.Contact)
async def create_contact_for_country(country_id: int,
                                     contact: schemas.ContactCreate,
                                     db: Session = Depends(get_db)):
    """Endpoint to create emergency contact based on country_id"""

    return crud.create_contact(db=db,
                               contact=contact,
                               country_id=country_id)


@router.put("/update_contact/{contact_id}", response_model=schemas.Contact)
async def update_contact(contact_id: int,
                         contact_update: schemas.ContactBase,
                         db: Session = Depends(get_db)):
    """Endpoint to update emergemcy contact based on its id"""

    return crud.update_contact(db, contact_id, contact_update)


@router.delete("/delete_contact/{contact_id}", response_model=None)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete emergency contact based on its id"""

    crud.delete_contact(db, contact_id)
    return {"message": "Contact deleted successfully"}
