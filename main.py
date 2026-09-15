from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models import BASE
from database import engine
from Routers import Applications,Auth,Companies,Interviews
from config import setting_obj, API_V1_PREFIX
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os 
import dotenv

limiter = Limiter(key_func=get_remote_address)


app = FastAPI(
    docs_url='/docs' if setting_obj.DEBUG else None,
    redoc_url='/redoc' if setting_obj.DEBUG else None,
    openapi_url='/openapi_json' if setting_obj.DEBUG else None,
    version='0.0.1',
    redirect_slashes=False,
    openapi_tags=None,
    contact={"name":"Anmol Patalay","email":"anmolpatalay@gmail.com","url":"https://www.linkedin.com/in/anmol-patalay-80b9a6328/"},
    title="Job Application Tracker",
    description="A REST API backend using FastAPI and MySQL to manage applied companies, job applications, and interview details for each company."
    
)

BASE.metadata.create_all(bind=engine)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)

app.include_router(Auth.router, prefix=API_V1_PREFIX)
app.include_router(Applications.router, prefix=API_V1_PREFIX)
app.include_router(Companies.router, prefix=API_V1_PREFIX)
app.include_router(Interviews.router, prefix=API_V1_PREFIX)


@app.get("/health")
async def get_health():
    return {"status":"healthy"}

# ALLOWED_ORIGINS = os.getenv(
#     "ALLOWED_ORIGINS",
#     "http://127.0.0.1:8000/"
# )


ALLOWED_ORIGINS = [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:8000").split(",")
    if o.strip()
]

if setting_obj.DEBUG and "http://127.0.0.1:8000" not in ALLOWED_ORIGINS:
    ALLOWED_ORIGINS.append("http://127.0.0.1:8000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE","PATCH"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=600,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/",include_in_schema=False)
async def root():
    return FileResponse("static/index.html")