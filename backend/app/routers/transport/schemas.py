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


class TransportBase(BaseModel):
    """Class that defines instance attributes"""

    name: str


class TransportCreate(TransportBase):
    """Class that passes instance attributes"""

    pass


class Transport(TransportBase):
    """Class that defines instance attributes"""

    id: int
    country: Country

    class Config:
        """Class that configures ORM mode"""

        from_attributes = True