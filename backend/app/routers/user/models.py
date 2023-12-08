#!/usr/bin/python3
"""Module that defines tables"""

import secrets
from .database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        String, event, DDL)


class User(Base):
    """class that defines User attributes"""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=True)
    status = Column(Boolean, default=True)
    user_type_id = Column(Integer, ForeignKey("user_type.id"), nullable=True)

    @staticmethod
    def generate_hash(password):
        """Function to hash password in database"""

        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        """Function to verify hashed password in database"""

        return sha256.verify(password, hash)


class UserInfo(Base):
    """Class that defines additional user information"""

    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)

    user = relationship('User', backref="user_info")


# Define the trigger function
trigger_function = DDL('''
CREATE OR REPLACE FUNCTION insert_user_info()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_info (user_id) VALUES (NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
''')


def insert_user_info(mapper, connection, target):
    """Function to add user details"""

    connection.execute(UserInfo.__table__.insert().values(user_id=target.id))


# Attach the trigger function to the 'after_insert' event of the User table
event.listen(User, 'after_insert', insert_user_info)


class ResetPasswordToken(Base):
    """Class that defines access tokens"""

    __tablename__ = "reset_password_token"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    token = Column(String, index=True)
    date_created = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_token():
        """Function to generate access token"""

        token = secrets.token_urlsafe(4)
        return sha256.hash(token)

    @staticmethod
    def verify_token(token, hash):
        """Function to verify access token"""

        return sha256.verify(token, hash)


class UserType(Base):
    """Class that defines types of users"""

    __tablename__ = "user_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True, index=True)

    user = relationship('User', backref="user_type")
