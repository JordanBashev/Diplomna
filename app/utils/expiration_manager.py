from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.models.db_models.card import Card
from app.models.db_models.ticket import TicketType
from app.models.db_models.user_ticket import UserTicket


scheduler = AsyncIOScheduler(timezone=ZoneInfo("Europe/Sofia"))

@scheduler.scheduled_job("interval", minutes=40)
async def clean_basic_tickets():
    async for db in get_db():
        await expire_ticket(db, TicketType.BASIC)

@scheduler.scheduled_job("interval", hours=1)
async def clean_hourly_tickets():
    async for db in get_db():
        await expire_ticket(db, TicketType.HOURLY)

@scheduler.scheduled_job("interval", days=1)
async def clean_tourist_tickets():
    async for db in get_db():
        await expire_ticket(db, TicketType.TOURIST)

@scheduler.scheduled_job("cron", hour=0, minute=0)
async def run_card_expiration():
    async for db in get_db():
        await expire_cards(db)


async def expire_ticket(db: AsyncSession, ticket_type: TicketType):
    now = datetime.now(timezone.utc)

    result = await db.execute(
        select(UserTicket).where(UserTicket.expiration_at < now)
    )
    tickets_to_expire = result.scalars().all()

    if not tickets_to_expire:
        return

    stmt = (
        delete(UserTicket)
        .where(UserTicket.expiration_at <= now)
        .where(UserTicket.ticket.has(type=ticket_type))
    )

    await db.execute(stmt)
    await db.commit()

async def expire_cards(db: AsyncSession):
    now = datetime.now(timezone.utc)

    result = await db.execute(
        select(Card).where(Card.expiration_at < now, Card.is_active == True)
    )
    cards_to_expire = result.scalars().all()

    if not cards_to_expire:
        return

    stmt = (
        update(Card)
        .where(Card.expiration_at < now)
        .where(Card.is_active == True)
        .values(is_active=False)
    )
    await db.execute(stmt)
    await db.commit()
