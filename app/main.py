from fastapi import FastAPI
from app.controller import users
from app.utils.lifespan_manager import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)