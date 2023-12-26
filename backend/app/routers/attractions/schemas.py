#!/usr/bin/python3
"""Module that defines orm schemas for tables"""

from typing import List
from pydantic import BaseModel


class CountryBase(BaseModel):
    """Class that defines instance attributes"""

    name: str


class CountryCreate(CountryBase):
    """Class that passes instance attributes"""

    pass


class Country(CountryBase):
    """Class that defines instance attributes"""

    id: int
    region_id: int

    class Config:
        """Class that configures ORM mode"""

        from_attributes = True


class RegionBase(BaseModel):
    """Class that defines instance attributes"""

    name: str


class RegionCreate(RegionBase):
    """Class that defines instance attributes"""

    name: str


class Region(RegionBase):
    """Class that defines instance attributes"""

    id: int
    is_active: bool
    countries: List[Country] = []

    class Config:
        """Class that configures ORM mode"""

        from_attributes = True


class Region_(RegionBase):
    """Class that defines instance attributes"""

    id: int

    class Config:
        """Class that configures ORM mode"""

        from_attributes = True


class ProvinceBase(BaseModel):
    """Class that defines instance attributes"""

    name: str


class ProvinceCreate(ProvinceBase):
    """Class that passes instance attributes"""

    pass


class Province(ProvinceBase):
    """Class that defines instance attributes"""

    id: int
    country: Country

    class Config:
        """Class that configures ORM mode"""

        from_attributes = True


class CityBase(BaseModel):
    name: str


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    country: Country
    province: Province

    class Config:
        from_attributes = True


class TourBase(BaseModel):
    name: str
    description: str
    contact: str


class TourCreate(TourBase):
    pass


class Tour(TourBase):
    id: int
    country: Country
    province: Province
    city: City

    class Config:
        from_attributes = True
