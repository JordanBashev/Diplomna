from sqlalchemy import Boolean, Column, Float, Integer, String
from app.database.db import Base
from sqlalchemy.orm import relationship

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    line_name = Column(String, nullable=False)
    gps_active = Column(Boolean, default=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    

