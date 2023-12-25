#!/usr/bin/python3
"""Module that defines tables"""

from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date


class Region(Base):
    """Class that defines regions attributes"""

    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    countries = relationship("Country", back_populates="region")


class Country(Base):
    """Class that defines countries attributes"""

    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"))

    region = relationship("Region", back_populates="countries")
    holidays = relationship("Holiday", back_populates="country")


class Holiday(Base):
    """Class that defines holiday attributes"""

    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    date = Column(Date)
    country_id = Column(Integer, ForeignKey("countries.id"))

    country = relationship("Country", back_populates="holidays")
