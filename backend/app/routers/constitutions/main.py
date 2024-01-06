#!/usr/bin/python3
"""Module that defines endpoints"""

from typing import List
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi import Depends, HTTPException, APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
import io

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/get_constitution/{country_id}",
            response_model=List[schemas.Constitution])
async def read_constitution_by_country(country_id: int,
                                       db: Session = Depends(get_db)):
    """Endpoint to read constitution based on country_id"""

    constitution = crud.get_constitution_by_country(db, country_id=country_id)
    if constitution:
        return StreamingResponse(io.BytesIO(constitution.content),
                                 media_type="application/pdf")
    raise HTTPException(status_code=404, detail="Constitution not found")


@router.get("/get_constitution_by_name",
            response_model=List[schemas.Constitution])
async def read_constitution_by_name(country_name: str,
                                    db: Session = Depends(get_db)):
    """Endpoint to read constitution based on country name"""

    constitution = crud.get_constitution_by_country_name(
            db, country_name=country_name)
    if constitution:
        return StreamingResponse(io.BytesIO(constitution.content),
                                 media_type="application/pdf")
    raise HTTPException(status_code=404, detail="Constitution not found")


@router.get("/constitution/{constitution_id}",
            response_model=schemas.Constitution)
async def read_constitution(constitution_id: int,
                            db: Session = Depends(get_db)):
    """Endpoint to read constitution based on its id"""

    db_constitution = crud.get_constitution(
            db, constitution_id=constitution_id)
    if db_constitution is None:
        raise HTTPException(status_code=404, detail="Constitution not found")
    return StreamingResponse(io.BytesIO(db_constitution.content),
                             media_type="application/pdf")


@router.post("/upload_constitution{country_id}")
async def upload_constitution(country_id: int, file: UploadFile = File(...),
                              db: Session = Depends(get_db)):
    """Endpoint to upload a constitution"""

    constitution_content = file.file.read()
    constitution_data = schemas.ConstitutionCreate(
            title=file.filename, content=constitution_content)
    db_constitution = crud.create_constitution(
            db, constitution_data, country_id)
    return {"message": "Constitution uploaded successfully",
            "constitution_id": db_constitution.id}


@router.put("/update_constitution/{constitution_id}",
            response_model=schemas.Constitution)
async def update_constitution(
        constitution_id: int, constitution_update: schemas.ConstitutionBase,
        db: Session = Depends(get_db)):
    """Endpoint to update constitution based on its id"""

    return crud.update_constitution(db, constitution_id, constitution_update)


@router.delete("/delete_constitution/{constitution_id}", response_model=None)
async def delete_constitution(constitution_id: int,
                              db: Session = Depends(get_db)):
    """Endpoint to delete constitution based on its id"""

    crud.delete_constitution(db, constitution_id)
    return {"message": "Constitution deleted successfully"}
