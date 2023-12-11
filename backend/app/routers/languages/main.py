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


@router.get("/get_languages", response_model=List[schemas.Language])
async def read_languages_by_country(country_id: int,
                                    skip: int = 0,
                                    limit: int = 100,
                                    db: Session = Depends(get_db)):
    """Endpoint to read languages based on country_id"""

    languages = crud.get_languages_by_country(db,
                                              country_id=country_id,
                                              skip=skip,
                                              limit=limit)
    return languages


@router.get("/language/{language_id}", response_model=schemas.Language)
async def read_language(language_id: int, db: Session = Depends(get_db)):
    """Endpoint to read language based on its id"""

    db_language = crud.get_language(db, language_id=language_id)
    if db_language is None:
        raise HTTPException(status_code=404, detail="Language not found")
    return db_language


@router.post("/create_language/{country_id}", response_model=schemas.Language)
async def create_language_for_country(country_id: int,
                                      language: schemas.LanguageCreate,
                                      db: Session = Depends(get_db)):
    """Endpoint to create language based on country_id"""

    return crud.create_language(db=db,
                                language=language,
                                country_id=country_id)


@router.put("/update_language/{language_id}", response_model=schemas.Language)
async def update_language(language_id: int,
                          language_update: schemas.LanguageBase,
                          db: Session = Depends(get_db)):
    """Endpoint to update language based on its id"""

    return crud.update_language(db, language_id, language_update)


@router.delete("/delete_language/{language_id}", response_model=None)
async def delete_language(language_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete language based on its id"""

    crud.delete_language(db, language_id)
    return {"message": "Language deleted successfully"}
