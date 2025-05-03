from datetime import time, timedelta, datetime, timezone
from zoneinfo import ZoneInfo
from sqlalchemy import delete, select

from app.models.db_models.card import Card
from app.models.db_models.user import User
from app.models.db_models.user_ticket import UserTicket
from app.models.db_models.ticket import Ticket, TicketType

from sqlalchemy.ext.asyncio import AsyncSession


class UsersRepository:
    def __init__(self, db_instance: AsyncSession) -> None:
        self.db: AsyncSession = db_instance

    async def add(self, user: User) -> None:
        self.db.add(user)
        await self.db.commit()


    async def edit(self, user: User, user_id: int) -> None:
        statement = select(User).where(User.id == user_id)

        result = await self.db.execute(statement)
        item: User = result.scalars().first()

        if not item:
            return

        item.email = user.email
        item.username = user.username
        item.hashed_password = user.hashed_password

        await self.db.commit()
        await self.db.refresh(item)

    
    async def delete(self, user_id: int) -> None:
        statement = select(User).where(User.id == user_id)

        result = await self.db.execute(statement)
        item: User = result.scalars().first()

        await self.db.delete(item)


    async def buy_ticket(self, ticket_id: int, user_id: int) -> None:
        statement = select(Ticket).where(Ticket.id == ticket_id)

        result = await self.db.execute(statement)
        chosen_ticket = result.scalars().first()

        if not chosen_ticket:
            raise ValueError("Invalid ticket ID")
        
        await self.db.execute(
            delete(UserTicket).where(UserTicket.user_id == user_id)
        )

        now: datetime = datetime.now(timezone.utc)

        if chosen_ticket.type == TicketType.BASIC:
            expires = now + timedelta(seconds=30)
        elif chosen_ticket.type == TicketType.TOURIST:
            expires = now + timedelta(days=1)
        elif chosen_ticket.type == TicketType.HOURLY:
            expires = now + timedelta(hours=1)
        else:
            raise ValueError("Unsupported ticket type")

        user_ticket = UserTicket(
            user_id=user_id,
            ticket_id=ticket_id,
            purchased_at=now,
            expiration_at=expires
        )

        self.db.add(user_ticket)
        await self.db.commit()


    async def buy_card(self, user_id: int) -> None:
        stmt = select(Card).where(Card.user_id == user_id)
        result = await self.db.execute(stmt)
        existing_card = result.scalar_one_or_none()

        if existing_card:
            raise ValueError("User has a card")

        new_card = Card(
            user_id=user_id,
            expiration_at=self.get_expiration_late_night(),
            is_active=True,
        )
    
        self.db.add(new_card)
        await self.db.commit()


    def get_expiration_late_night(self, days_from_now=31, tz_str="Europe/Sofia") -> datetime:
        now = datetime.now(ZoneInfo(tz_str))
        target_date = now.date() + timedelta(days=days_from_now)

        expiration_dt = datetime.combine(target_date, time(23, 59, 59), tzinfo=ZoneInfo(tz_str))

        return expiration_dt.astimezone(ZoneInfo("UTC"))