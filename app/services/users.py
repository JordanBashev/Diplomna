from app.models.schemas.users import UserAdd, UserEdit


from app.models.db_models.user import User
from app.models.db_models.user_ticket import UserTicket
from app.models.db_models.ticket import Ticket, TicketType


from app.repositories.users import UsersRepository


class UsersServices:
    def __init__(self, db_instance) -> None:
        self.db = db_instance
        self.user_repo = UsersRepository(db_instance)

    async def add(self, user_data: UserAdd) -> None:
        if user_data:
            user = User(**user_data.model_dump())
            await self.user_repo.add(user)

    async def update(self, user_data: UserEdit, user_id: int) -> None:
        if user_data:
            user = User(**user_data.model_dump())
            await self.user_repo.edit(user, user_id)

    async def delete(self, user_id: int) -> None:
        if user_id:
            await self.user_repo.delete(user_id)

    async def buy_ticket(self, ticket_id: int, user_id: int) -> None:
        if ticket_id and user_id:
            await self.user_repo.buy_ticket(ticket_id, user_id)

    async def buy_card(self, user_id: int) -> None:
        if user_id:
            await self.user_repo.buy_card(user_id)

