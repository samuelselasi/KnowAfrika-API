#!/usr/bin/python3
"""Module that defines orm schemas for tables"""

from typing import Optional
from pydantic import BaseModel
from app.routers.user.schemas import User, UserBase


class Auth(UserBase):
    """Class that defines private instance attributes"""

    password: str


class AuthResponse(BaseModel):
    """Class that defines public instance attributes"""

    access_token: str
    refresh_token: str
    user: User

    class Config:
        """Class to configure ORM mode"""

        orm_mode = True


class Token(BaseModel):
    """Class that defines public token attributes"""

    access_token: Optional[str]
    refresh_token: Optional[str]
