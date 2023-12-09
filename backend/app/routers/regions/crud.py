#!/usr/bin/python3
"""Module that defines CRUD functions"""

from . import models, schemas
from fastapi import HTTPException
from sqlalchemy.orm import Session


def get_region_by_id(db: Session, region_id: int):
    """Function to return region and its countries based on id"""

    return db.query(models.Region).filter(models.Region.id ==
                                          region_id).first()


def get_region_by_name(db: Session, region_name: str):
    """Function to return region and its countries based on name"""

    return db.query(models.Region).filter(models.Region.name ==
                                          region_name).first()


def get_regions_and_countries(db: Session, skip: int = 0, limit: int = 100):
    """Function to return all regions and their countries"""

    return db.query(models.Region).offset(skip).limit(limit).all()


def get_regions(db: Session, skip: int = 0, limit: int = 100):
    """Function to return all regions"""

    regions = db.query(models.Region).offset(skip).limit(limit).all()
    region_info = [{"id": region.id,
                    "name": region.name} for region in regions]
    return region_info


def create_region(db: Session, region: schemas.RegionCreate):
    """Function to create a region"""

    db_region = models.Region(name=region.name)
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region


def update_region(db: Session, region_id: int,
                  region_update: schemas.RegionBase):
    """Function to update a region based on its id"""

    db_region = get_region_by_id(db, region_id=region_id)
    if db_region:
        for key, value in region_update.dict().items():
            setattr(db_region, key, value)
        db.commit()
        db.refresh(db_region)
        return db_region
    else:
        raise HTTPException(status_code=404, detail="Region not found")


def delete_region(db: Session, region_id: int):
    """Function to delete a region based on its id"""

    db_region = get_region_by_id(db, region_id=region_id)
    if db_region:
        db.delete(db_region)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Region not found")
