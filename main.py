from fastapi import FastAPI
from models import BASE
from database import engine
from Routers import Applications,Auth,Companies,Interviews
app= FastAPI()

BASE.metadata.create_all(bind=engine)

app.include_router(Auth.router)
app.include_router(Applications.router)
app.include_router(Companies.router)
app.include_router(Interviews.router)