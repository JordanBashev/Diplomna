from dataclasses import dataclass
from enum import Enum
from sqlalchemy import Column, Integer, String
from app.database.db import Base
from sqlalchemy.orm import relationship

@dataclass(frozen=True)
class TicketType:
    BASIC = "basic"
    TOURIST = "tourist"
    HOURLY = "hourly"


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)

    user_tickets = relationship("UserTicket", back_populates="ticket")
    

