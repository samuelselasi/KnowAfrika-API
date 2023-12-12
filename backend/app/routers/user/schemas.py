#!/usr/bin/python3
"""Module that defines orm schemas for tables"""

from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Class that defines instance attributes"""

    email: EmailStr


class UserCreate(UserBase):
    """Class that defines instance attributes"""

    password: Optional[str]
    user_type_id: int
    status: Optional[bool]


class UserUpdate(BaseModel):
    """Class that defines instance attributes"""

    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]


class ResetPassword(BaseModel):
    """Class that defines instance attributes"""

    password: str
    code: Optional[str]


class ChangePassword(BaseModel):
    """Class that defines instance attributes"""

    email: str
    password: str


class User(UserBase):
    """Class that defines instance attributes"""

    id: int
    user_type_id: int

    class Config:
        """Class that configures ORM mode"""

        from_attributes = True
