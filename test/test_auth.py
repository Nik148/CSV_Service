from httpx import AsyncClient
from sqlalchemy import select
import pytest
from .conftest import async_session_maker
from app.model import User


@pytest.mark.asyncio
async def test_register(ac: AsyncClient):
    response = await ac.post("/registration", json={
        "login": "lake",
        "password": "123pool"
    })
    
    assert response.status_code == 200
    async with async_session_maker() as session:
        user = await session.execute(select(User).where(User.login == "lake"))
        user: User = user.scalar()
        assert user
    
    response = await ac.post("/registration", json={
        "login": "lake",
        "password": "pool"
    })
    
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_login(ac: AsyncClient):
    response = await ac.post("/login", json={
        "login": "nik",
        "password": "123"
    })
    assert response.status_code == 400

    response = await ac.post("/login", json={
        "login": "lake",
        "password": "123"
    })
    assert response.status_code == 400

    response = await ac.post("/login", json={
        "login": "lake",
        "password": "123pool"
    })

    assert response.status_code == 200