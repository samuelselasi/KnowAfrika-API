#!/usr/bin/python3
"""Module that defines CRUD functions"""

from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session


def get_language(db: Session, language_id: int):
    """Function to get language based on its id"""

    return db.query(models.Language).filter(models.Language.id ==
                                            language_id).first()


def get_languages_by_country(db: Session, country_id: int, skip: int = 0,
                             limit: int = 100):
    """Function to get language based on country id"""

    return db.query(models.Language).filter(models.Language.country_id ==
                                            country_id).offset(skip).limit(
                                                    limit).all()


def create_language(db: Session, language: schemas.LanguageCreate,
                    country_id: int):
    """Function to create language for a country"""

    db_language = models.Language(**language.dict(), country_id=country_id)
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language


def update_language(db: Session, language_id: int,
                    language_update: schemas.LanguageBase):
    """Function to update language of a country based on its id"""

    db_language = get_language(db, language_id=language_id)
    if db_language:
        for key, value in language_update.dict().items():
            setattr(db_language, key, value)
        db.commit()
        db.refresh(db_language)
        return db_language
    else:
        raise HTTPException(status_code=404, detail="Language not found")


def delete_language(db: Session, language_id: int):
    """Funtion to delete language based on its id"""

    db_language = get_language(db, language_id=language_id)
    if db_language:
        db.delete(db_language)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Language not found")
