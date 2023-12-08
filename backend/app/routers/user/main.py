#!/usr/bin/python3
"""Module that defines endpoints for users"""

from typing import List
from sqlalchemy.orm import Session
from . import crud, models, schemas
from app.oauth2 import oauth2_scheme
from .database import SessionLocal, engine
from fastapi import Depends, HTTPException, APIRouter, status

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/get_users", response_model=List[schemas.User])
async def read_all_users(db: Session = Depends(get_db)):
    """Endpoint to read all users"""

    return await crud.read_users(db)


@router.get("/get/{id}", response_model=schemas.User)
async def read_a_user_by_id(id: int, db: Session = Depends(get_db)):
    """Endpoint to read user by id"""

    user = await crud.read_user_by_id(id, db)
    if not user:
        raise HTTPException(
                status_code=404,
                detail="user with id: {} was not found".format(id))
    return user


@router.get("/{email}/", response_model=schemas.User)
async def read_user_by_email(email: str, db: Session = Depends(get_db)):
    """Endpoint to read user by email"""

    user = await crud.read_user_by_email(email, db)
    if not user:
        raise HTTPException(
                status_code=404,
                detail="user with email: {} was not found".format(email))
    return user


@router.get("/verify_hash")
async def verify_hash_details(code: str, db: Session = Depends(get_db)):
    """Endpoint to verify hash code"""

    return await crud.read_hash_code(code, db)


@router.get("/read_hash_table")
async def read_hash_table(db: Session = Depends(get_db)):
    """Endpoint to read hash codes"""

    return await crud.read_hash_table(db)


@router.post("/create_user", response_model=schemas.User)
async def create_user(payload: schemas.UserCreate,
                      db: Session = Depends(get_db)):
    """Endpoint to create a user"""

    return await crud.create_user(payload, db)


@router.post("/verify/password")
async def verify_password(
        id: int, payload: schemas.ResetPassword,
        db: Session = Depends(get_db)):
    """Endpoint to verify password"""

    return await crud.verify_password(id, payload, db)


@router.patch("/update/{id}", response_model=schemas.User, status_code=202)
async def update_user(
        id: int, payload: schemas.UserUpdate,
        db: Session = Depends(get_db)):
    """Endpoint to update user details"""

    return await crud.update_user(id, payload, db)


@router.patch("/{id}/password", status_code=status.HTTP_202_ACCEPTED)
async def update_password(
        id: int, payload: schemas.ResetPassword,
        db: Session = Depends(get_db)):
    """Endpoint to update user password"""

    return await crud.reset_password(id, payload, db)


@router.patch("/password", status_code=status.HTTP_202_ACCEPTED)
async def update_password_(email: str, payload: schemas.ResetPassword,
                           db: Session = Depends(get_db)):
    """Endpoint to update user password"""

    return await crud.reset_password_(email, payload, db)


@router.put("/change/password")
async def change_password(payload: schemas.ChangePassword,
                          db: Session = Depends(get_db)):
    """Endpoint tochange user password"""

    return await crud.change_password(payload.email, payload.password, db)


@router.delete("/delete/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    """Endpoint to delete user based on id"""

    return await crud.delete_user(id, db)
