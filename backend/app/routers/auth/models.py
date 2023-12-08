#!/usr/bin/python3
"""Module that defines tables"""

from app import utils
from .database import Base
from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime


class ResetPasswordCodes(Base):
    """Class that defines reset password table instances"""

    __tablename__ = 'reset_password_codes'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String, unique=True)
    user_id = Column(Integer, unique=True)
    user_email = Column(String, unique=True)
    status = Column(Boolean, nullable=False, default=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    @staticmethod
    def generate_code():
        """Function that returns hashed code"""

        return utils.gen_alphanumeric_code(32)


class RevokedToken(Base):
    """Class that defines revoked tokens table instances"""

    __tablename__ = 'revoked_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    jti = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)
