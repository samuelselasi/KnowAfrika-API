#!/usr/bin/python3
"""Module that defines endpoints functions"""

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


@router.get("/get_regions", response_model=List[schemas.Region_])
async def read_regions(skip: int = 0,
                       limit: int = 100,
                       db: Session = Depends(get_db)):
    """Endpoint to read all regions"""

    regions = crud.get_regions(db, skip=skip, limit=limit)
    return regions


@router.get("/get_regions_countries", response_model=List[schemas.Region])
async def read_regions_and_countries(skip: int = 0,
                                     limit: int = 100,
                                     db: Session = Depends(get_db)):
    """Endpoint to read all regions and their countries"""

    regions = crud.get_regions_and_countries(db, skip=skip, limit=limit)
    return regions


@router.get("/get_region_by_id/{region_id}", response_model=schemas.Region)
async def read_region_id(region_id: int, db: Session = Depends(get_db)):
    """Endpoint to read region based on its id"""

    db_region = crud.get_region_by_id(db, region_id=region_id)
    if db_region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return db_region


@router.get("/get_region_by_name/region_name", response_model=schemas.Region)
async def read_region_name(region_name: str, db: Session = Depends(get_db)):
    """Endpoint to read region based on its name"""

    db_region = crud.get_region_by_name(db, region_name=region_name)
    if db_region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return db_region


@router.post("/create_region", response_model=schemas.Region)
async def create_region(region: schemas.RegionCreate,
                        db: Session = Depends(get_db)):
    """Endpoint to create a region"""

    db_region = crud.get_region_by_name(db, region_name=region.name)
    if db_region:
        raise HTTPException(status_code=400,
                            detail="Name already registered")
    return crud.create_region(db=db, region=region)


@router.put("/update_region/{region_id}", response_model=schemas.Region)
async def update_region(region_id: int,
                        region_update: schemas.RegionBase,
                        db: Session = Depends(get_db)):
    """Endpoint to update region based on its id"""

    return crud.update_region(db, region_id, region_update)


@router.delete("/delete_region/{region_id}", response_model=None)
async def delete_region(region_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete region based on its id"""

    crud.delete_region(db, region_id)
    return {"message": "Region deleted successfully"}
