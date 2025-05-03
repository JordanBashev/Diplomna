from typing import Annotated
from fastapi import APIRouter, Depends

from app.deps.deps import get_user_service
from app.services.users import UsersServices
from app.models.schemas.users import UserAdd, UserEdit

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/")
async def create_user(user_data: UserAdd, user_service: Annotated[UsersServices, Depends(get_user_service)]) -> None:
    await user_service.add(user_data)


@router.patch("/{user_id}")
async def edit_user(user_id: int, user_data: UserEdit, user_service: Annotated[UsersServices, Depends(get_user_service)]) -> None:
    await user_service.update(user_data, user_id)


@router.post("/{user_id}/purchase-tickets")
async def purchase_ticket(user_id: int, ticket_id, user_service: Annotated[UsersServices, Depends(get_user_service)]) -> None:
    await user_service.buy_ticket(ticket_id, user_id)


@router.post("/{user_id}/purchase-cards")
async def purchase_card(user_id: int, user_service: Annotated[UsersServices, Depends(get_user_service)]) -> None:
    await user_service.buy_card(user_id)

