from sqlalchemy import Column, Integer, String
from app.database.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    refresh_token = Column(String, nullable=True) # will be foreign key problembly
    card = relationship("Card", back_populates="user", uselist=False, cascade="all, delete-orphan")
    

