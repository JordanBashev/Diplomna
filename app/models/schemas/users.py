from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserAdd(UserBase):
    hashed_password: str

class UserEdit(UserBase):
    hashed_password: str

class Config:
        orm_mode = True