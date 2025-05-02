from pydantic import BaseModel

class CardBase(BaseModel):
    type: str

class CardAdd(CardBase):
    pass

class Config:
        orm_mode = True