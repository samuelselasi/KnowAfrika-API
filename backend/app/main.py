#!/usr/bin/python3
"""Module to initialize routers and endpoints"""

from fastapi import FastAPI
from app.routers.auth import main as auth
from app.routers.user import main as user
from app.routers.regions import main as regions
from app.routers.countries import main as countries

app = FastAPI(debug=True)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(user.router, tags=["Users"])
app.include_router(regions.router, tags=["Regions"])
app.include_router(countries.router, tags=["Countries"])


@app.get("/")
async def root():
    """Function that returns a default message when the root url is hit"""

    return {"message": "Welcome to KnowAfrika API. Hit /docs for swagger"}
