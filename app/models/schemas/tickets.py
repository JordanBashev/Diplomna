from pydantic import BaseModel

class TicketBase(BaseModel):
    type: str

class TicketAdd(TicketBase):
    pass

class Config:
        orm_mode = True