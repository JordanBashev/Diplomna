from sqlalchemy import Column, Index, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    expiration_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=False)

    user = relationship("User", back_populates="card")

    __table_args__ = (
        Index("ix_cards_expiration_active", "expiration_at", "is_active"),
    )