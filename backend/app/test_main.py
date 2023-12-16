#!/usr/bin/python3
"""Module to test main"""

import pytest
from .main import app
from httpx import AsyncClient


@pytest.mark.anyio
async def test_root():
    """Function to test root function"""

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {
            "message": "Welcome to KnowAfrika API. Hit /docs for swagger"}
