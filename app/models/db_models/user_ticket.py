import datetime
from enum import Enum
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from app.database.db import Base
from sqlalchemy.orm import relationship

class UserTicket(Base):
    __tablename__ = 'user_tickets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)  # Enforces 1 ticket per user
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)
    purchased_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    expiration_at = Column(DateTime)

    ticket = relationship("Ticket", back_populates="user_tickets")