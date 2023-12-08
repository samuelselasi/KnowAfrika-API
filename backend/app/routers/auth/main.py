#!/usr/bin/python3
"""Module that defines endpoints for authentication"""

from sqlalchemy.orm import Session
from . import crud, models, schemas
from app.oauth2 import oauth2_scheme
from .database import SessionLocal, engine
from fastapi import Depends, BackgroundTasks, APIRouter

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/current_user", response_model=schemas.User)
async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: Session = Depends(get_db)):
    """Endpoint to get current user logged in"""

    return await crud.get_current_user(token, db)


@router.post("/login", response_model=schemas.AuthResponse)
async def authenticate(payload: schemas.Auth, db: Session = Depends(get_db)):
    """Endpoint to log in user with email and password"""

    return await crud.authenticate(payload, db)


@router.post("/logout")
async def logout(payload: schemas.Token, db: Session = Depends(get_db)):
    """Endpoint to log out user with token"""

    return await crud.revoke_token(payload, db)


@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(payload: schemas.Token,
                        db: Session = Depends(get_db)):
    """Function to refresh expired session with token"""

    return await crud.refresh_token(payload, db)


@router.post("/request")
async def request_password_reset(payload: schemas.UserBase,
                                 background_tasks: BackgroundTasks,
                                 db: Session = Depends(get_db)):
    """Endpoint to request reset password code with email"""

    return await crud.request_password_reset_(payload, db, background_tasks)
