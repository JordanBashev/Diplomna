import os
import sys
import asyncio


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import select
from app.models.db_models.ticket import Ticket, TicketType
from app.database.db import engine, Base, get_db
from app.utils.password_hasher import hash_password

async def populate_tickets_table():
    async for session in get_db():
        async with session.begin():
            result = await session.execute(select(Ticket))
            existing_tickets = result.scalars().all()

            if existing_tickets:
                print("Tickets already exist. Skipping.")
                return

            tickets = [
                Ticket(type=TicketType.BASIC),
                Ticket(type=TicketType.TOURIST),
                Ticket(type=TicketType.HOURLY),
            ]

            session.add_all(tickets)
            print("Tickets populated.")


async def populate_user_table():
    async for session in get_db():
        async with session.begin():
            result = await session.execute(select(User))
            existing_users = result.scalars().all()

            if existing_users:
                print("Users already exist. Skipping.")
                return
            
            password = "Passw0rd123"

            users = [
                User(username="Pesho", email="pesho@email.com", hashed_password=hash_password(password=password)),
                User(username="Gosho", email="gosho@email.com", hashed_password=hash_password(password=password)),
                User(username="Tosho", email="tosho@email.com", hashed_password=hash_password(password=password))
            ]

            session.add_all(users)
            print("Tickets populated.")


async def reset_database():
    async with engine.begin() as conn:
        print("Dropping all tables...")
        await conn.run_sync(Base.metadata.drop_all)

        print("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)

        await populate_tickets_table()
        await populate_user_table()

if __name__ == "__main__":

    from app.models.db_models.user import User
    from app.models.db_models.ticket import Ticket
    from app.models.db_models.user_ticket import UserTicket
    from app.models.db_models.card import Card

    asyncio.run(reset_database())