from fastapi import Depends

from app.database.db import AsyncSessionLocal


async def get_database_instance():
    async with AsyncSessionLocal() as session:
        yield session