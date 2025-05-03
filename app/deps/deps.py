from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db_instance import get_database_instance
from app.services.users import UsersServices


async def get_user_service(db_instance: Annotated[AsyncSession, Depends(get_database_instance)]) -> UsersServices:
    return UsersServices(db_instance)