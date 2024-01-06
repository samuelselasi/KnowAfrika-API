#!/usr/bin/python3
"""Module that defines endpoints for attractions"""

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


@router.get("/get_attraction_by_country/{country_id}",
            response_model=List[schemas.Tour])
async def read_attractions_by_country(country_id: int,
                                      skip: int = 0,
                                      limit: int = 100,
                                      db: Session = Depends(get_db)):
    """Endpoint to read tourist attractions with country id"""

    tours = crud.get_tours_by_country(db, country_id=country_id,
                                      skip=skip, limit=limit)
    return tours


@router.get("/get_attractions_by_province/{province_id}",
            response_model=List[schemas.Tour])
async def read_attractions_by_province(province_id: int, skip: int = 0,
                                       limit: int = 100,
                                       db: Session = Depends(get_db)):
    """Endpoint to read attractions with province id"""

    tours = crud.get_tours_by_province(db, province_id=province_id,
                                       skip=skip, limit=limit)
    return tours


@router.get("/get_attractions_by_city/{city_id}",
            response_model=List[schemas.Tour])
async def read_attractions_by_city(city_id: int, skip: int = 0,
                                   limit: int = 100,
                                   db: Session = Depends(get_db)):
    """Endpoint to read attractions with city id"""

    a = crud.get_tours_by_city(db, city_id=city_id, skip=skip, limit=limit)
    return a


@router.get(
        "/get_attractions_by_country_and_province/{country_id}/{province_id}",
        response_model=List[schemas.Tour])
async def read_attractions_by_country_and_province(
        country_id: int, province_id: int,
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Endpoint to read attractions with country id and province id"""

    tours = crud.get_tours_by_country_and_province(db,
                                                   country_id=country_id,
                                                   province_id=province_id,
                                                   skip=skip, limit=limit)
    return tours


@router.get("/get_tours/{country_id}/{province_id}/{city_id}",
            response_model=List[schemas.Tour])
async def read_attractions_by_country_province_city(country_id: int,
                                                    province_id: int,
                                                    city_id: int,
                                                    skip: int = 0,
                                                    limit: int = 100,
                                                    db: Session = Depends(
                                                        get_db)):
    """Endpoint to read attractions with country_id, province_id & city_id"""

    a = crud.get_tours_by_country_and_province_and_city(
            db, country_id=country_id, province_id=province_id,
            city_id=city_id, skip=skip, limit=limit)
    return a


@router.get("/read_attraction/{tour_id}", response_model=schemas.Tour)
async def read_attraction(tour_id: int, db: Session = Depends(get_db)):
    """Endpoint to read attraction based on its id"""

    db_attraction = crud.get_tour(db, tour_id=tour_id)
    if db_attraction is None:
        raise HTTPException(status_code=404, detail="Attraction not found")
    return db_attraction


@router.get("/get_attraction_by_name", response_model=schemas.Tour)
async def read_attraction_by_name(tour_name: str,
                                  db: Session = Depends(get_db)):
    """Endpoint to read tourist attraction based on its name"""

    db_tour = crud.get_tour_by_name(db, tour_name=tour_name)
    if db_tour is None:
        raise HTTPException(status_code=404, detail="Attraction not found")
    return db_tour


@router.post("/create_attraction/{country_id}/{province_id}/{city_id}",
             response_model=schemas.Tour)
async def create_attraction_for_country(country_id: int,
                                        province_id: int, city_id: int,
                                        tour: schemas.TourCreate,
                                        db: Session = Depends(get_db)):
    """Endpoint to create attraction with country_id, province_id & city_id"""

    return crud.create_tour(db=db, tour=tour, country_id=country_id,
                            province_id=province_id, city_id=city_id)


@router.put("/update_attraction/{tour_id}", response_model=schemas.Tour)
async def update_attraction(tour_id: int,
                            tour_update: schemas.TourBase,
                            db: Session = Depends(get_db)):
    """Endpoint to update attraction based in its id"""

    return crud.update_tour(db, tour_id, tour_update)


@router.delete("/delete_attraction/{tour_id}", response_model=None)
async def delete_attraction(tour_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete attraction based on its id"""

    crud.delete_tour(db, tour_id)
    return {"message": "Tourist attraction deleted successfully"}
