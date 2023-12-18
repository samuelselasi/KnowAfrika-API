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


@router.get("/get_flag/{country_id}", response_model=List[schemas.Flag])
async def read_flag_by_country(country_id: int,
                               db: Session = Depends(get_db)):
    """Endpoint to read flag based on country_id"""

    flag = crud.get_flag_by_country(db, country_id=country_id)
    if flag:
        return StreamingResponse(io.BytesIO(flag.content),
                                 media_type="image/png")
    raise HTTPException(status_code=404, detail="Flag not found")


@router.get("/get_flag_by_name", response_model=List[schemas.Flag])
async def read_flag_by_name(country_name: str,
                            db: Session = Depends(get_db)):
    """Endpoint to read flag based on country name"""

    flag = crud.get_flag_by_country_name(db, country_name=country_name)
    if flag:
        return StreamingResponse(io.BytesIO(flag.content),
                                 media_type="image/png")
    raise HTTPException(status_code=404, detail="Flag not found")


@router.get("/flag/{flag_id}", response_model=schemas.Flag)
async def read_flag(flag_id: int, db: Session = Depends(get_db)):
    """Endpoint to read flag based on its id"""

    db_flag = crud.get_flag(db, flag_id=flag_id)
    if db_flag is None:
        raise HTTPException(status_code=404, detail="Flag not found")
    return StreamingResponse(io.BytesIO(db_flag.content),
                             media_type="image/png")


@router.post("/upload_flag{country_id}")
async def upload_flag(country_id: int, file: UploadFile = File(...),
                      db: Session = Depends(get_db)):
    """Endpoint to upload a flag"""

    flag_content = file.file.read()
    flag_data = schemas.FlagCreate(title=file.filename, content=flag_content)
    db_flag = crud.create_flag(db, flag_data, country_id)
    return {"message": "Flag uploaded successfully", "flag_id": db_flag.id}


@router.put("/update_flag/{flag_id}", response_model=schemas.Flag)
async def update_flag(flag_id: int, flag_update: schemas.FlagBase,
                      db: Session = Depends(get_db)):
    """Endpoint to update flag based on its id"""

    return crud.update_flag(db, flag_id, flag_update)


@router.delete("/delete_flag/{flag_id}", response_model=None)
async def delete_flag(flag_id: int, db: Session = Depends(get_db)):
    """Endpoint to delete flag based on its id"""

    crud.delete_flag(db, flag_id)
    return {"message": "Flag deleted successfully"}
