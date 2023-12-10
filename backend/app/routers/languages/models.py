#!/usr/bin/python3
"""Module that defines tables"""

from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


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
    languages = relationship("Language", back_populates="country")


class Language(Base):
    """Class that defines language attributes"""

    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    form = Column(String)
    country_id = Column(Integer, ForeignKey("countries.id"))

    country = relationship("Country", back_populates="languages")
