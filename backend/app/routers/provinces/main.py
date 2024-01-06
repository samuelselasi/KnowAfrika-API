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


@router.get("/get_provinces", response_model=List[schemas.Province])
async def read_provinces_by_country(country_id: int,
                                    skip: int = 0,
                                    limit: int = 100,
                                    db: Session = Depends(get_db)):
    """Endpoint to read provinces based on country_id"""

    provinces = crud.get_provinces_by_country(db,
                                              country_id=country_id,
                                              skip=skip,
                                              limit=limit)
    return provinces


@router.get("/get_provinces_by_country_name",
            response_model=List[schemas.Province])
async def read_provinces_by_country_name(country_name: str,
                                         skip: int = 0,
                                         limit: int = 100,
                                         db: Session = Depends(get_db)):
    """Endpoint to read provinces based on country name"""

    provinces = crud.get_provinces_by_country_name(db,
                                                   country_name=country_name,
                                                   skip=skip,
                                                   limit=limit)
    return provinces


@router.get("/province/{province_id}", response_model=schemas.Province)
async def read_province(province_id: int, db: Session = Depends(get_db)):
    """Endpoint to read province based on its id"""

    db_province = crud.get_province(db, province_id=province_id)
    if db_province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    return db_province


@router.get("/get_province_by_name", response_model=schemas.Province)
async def read_province_by_name(
        province_name: str, db: Session = Depends(get_db)):
    """Endpoint to read province based on its name"""

    db_province = crud.get_province_by_name(db, province_name=province_name)
    if db_province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    return db_province


@router.post("/create_province/{country_id}", response_model=schemas.Province)
async def create_province_for_country(country_id: int,
                                      province: schemas.ProvinceCreate,
                                      db: Session = Depends(get_db)):
    """Endpoint to create province based on country_id"""

    return crud.create_province(db=db,
                                province=province,
                                country_id=country_id)


@router.put("/update_province/{province_id}", response_model=schemas.Province)
async def update_province(province_id: int,
                          province_update: schemas.ProvinceBase,
                          db: Session = Depends(get_db)):
    """Endpoint to update province based on its id"""

    return crud.update_province(db, province_id, province_update)


@router.delete("/delete_province/{province_id}", response_model=None)
async def delete_province(province_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete province based on its id"""

    crud.delete_province(db, province_id)
    return {"message": "Province deleted successfully"}
