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
    provinces = relationship("Province", back_populates="country")
    cities = relationship("City", back_populates="country")


class Province(Base):
    """Class that defines province attributes"""

    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country_id = Column(Integer, ForeignKey("countries.id"))

    country = relationship("Country", back_populates="provinces")
    cities = relationship("City", back_populates="province")


class City(Base):
    """Class that defines city attributes"""

    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"))
    province_id = Column(Integer, ForeignKey("provinces.id"))
    name = Column(String, index=True)

    country = relationship("Country", back_populates="cities")
    province = relationship("Province", back_populates="cities")
