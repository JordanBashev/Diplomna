import calendar
from datetime import time, timedelta, datetime, timezone
from zoneinfo import ZoneInfo
from sqlalchemy import delete, select

from app.models.db_models.driver import Driver

from sqlalchemy.ext.asyncio import AsyncSession

class DriverRepository:
    def __init__(self, db_instance: AsyncSession):
        self.db = db_instance

    async def add(self, driver: Driver):
        self.db.add(driver)
        await self.db.commit()


    async def edit(self, driver: Driver, driver_id: int):
        statement = select(Driver).where(Driver.id == driver_id)

        result = await self.db.execute(statement)
        item: Driver = result.scalars().first()

        item.line_name = driver.line_name

        await self.db.commit()
        await self.db.refresh(item)

    
    async def delete(self, driver_id: int):
        statement = select(Driver).where(Driver.id == driver_id)

        result = await self.db.execute(statement)
        item: Driver = result.scalars().first()

        self.db.delete(item)