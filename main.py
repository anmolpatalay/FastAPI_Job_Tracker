from fastapi import FastAPI
from models import BASE
from database import engine
from Routers import Applications,Auth,Companies,Interviews
from config import setting_obj

app = FastAPI(
    docs_url='/docs' if setting_obj.DEBUG else None,
    redoc_url='/redoc' if setting_obj.DEBUG else None,
    openapi_url='/openapi_json' if setting_obj.DEBUG else None,
    version='0.0.1',
    openapi_tags=None,
    contact={"name":"Anmol Patalay","email":"anmolpatalay@gmail.com","url":"https://www.linkedin.com/in/anmol-patalay-80b9a6328/"},
    title="Job Application Tracker",
    description="A REST API backend using FastAPI and MySQL to manage applied companies, job applications, and interview details for each company."
    
)

BASE.metadata.create_all(bind=engine)

app.include_router(Auth.router)
app.include_router(Applications.router)
app.include_router(Companies.router)
app.include_router(Interviews.router)

@app.get("/health")
async def get_health():
    return {"ststus":"healthy"}