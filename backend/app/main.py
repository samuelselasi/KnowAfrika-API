#!/usr/bin/python3
"""Module to initialize routers and endpoints"""

from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.routers.auth import main as auth
from app.routers.user import main as user
from app.routers.regions import main as regions
from app.routers.countries import main as countries
from app.routers.provinces import main as provinces
from app.routers.cities import main as cities
from app.routers.currencies import main as currencies
from app.routers.languages import main as languages
from app.routers.flags import main as flags
from app.routers.holidays import main as holidays
from app.routers.attractions import main as attractions
from app.routers.constitutions import main as constitutions
from app.routers.transport import main as transport
from app.routers.timezones import main as timezones

app = FastAPI(debug=True)
app.mount("/templates",
          StaticFiles(directory="../frontend/web_static"),
          name="templates")

# templates = Jinja2Templates(directory="templates")
templates = Jinja2Templates(
        directory=str(Path(__file__).parent / "templates"))

app.include_router(auth.router, tags=["Authentication"])
app.include_router(user.router, tags=["Users"])
app.include_router(regions.router, tags=["Regions"])
app.include_router(countries.router, tags=["Countries"])
app.include_router(provinces.router, tags=["Provinces"])
app.include_router(cities.router, tags=["Cities"])
app.include_router(attractions.router, tags=["Tourist Attractions"])
app.include_router(currencies.router, tags=["Currencies"])
app.include_router(languages.router, tags=["Languages"])
app.include_router(flags.router, tags=["Flags"])
app.include_router(holidays.router, tags=["Holidays"])
app.include_router(constitutions.router, tags=["Constitutions"])
app.include_router(transport.router, tags=["Transportation"])
app.include_router(timezones.router, tags=["Time-zones"])


@app.get("/")
async def root():
    """Function that returns a default message when the root url is hit"""

    return {"message": "Welcome to KnowAfrika API. Hit /docs for swagger"}


@app.get("/landing_page")
def landing_page(request: Request):
    """Function that uses the templates instance to render landing page"""

    return templates.TemplateResponse("landing_page.html",
                                      {"request": request})


@app.get("/technical_documentation")
def technical_documentation(request: Request):
    """Function that uses the templates instance to render tech-doc page"""

    return templates.TemplateResponse("tech_doc.html",
                                      {"request": request})
