#!/usr/bin/python3
"""Module that defines tables"""

from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (Boolean, Column, ForeignKey,
                        Integer, String, LargeBinary)


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
    flags = relationship("Flag", back_populates="country")


class Flag(Base):
    """Class that defines flag attributes"""

    __tablename__ = "flags"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(LargeBinary)
    country_id = Column(Integer, ForeignKey("countries.id"))

    country = relationship("Country", back_populates="flags")
