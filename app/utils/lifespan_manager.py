from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.database.db import get_db
from app.models.db_models.ticket import TicketType
from app.utils.expiration_manager import expire_cards, expire_ticket, scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    print("Schedular Initiated!")

    async for db in get_db():
        await expire_cards(db)
        await expire_ticket(db, TicketType.BASIC)
        await expire_ticket(db, TicketType.HOURLY)
        await expire_ticket(db, TicketType.TOURIST)

    yield 

    scheduler.shutdown()
    print("Schedular Stopped")
