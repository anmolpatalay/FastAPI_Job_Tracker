from fastapi import APIRouter,Depends,HTTPException
from starlette import status
from models import Applications,Companies
from database import get_db
from sqlalchemy.orm import Session
from Routers.Auth import current_user
from pydantic import BaseModel
from datetime import date
from typing import Annotated,Literal
from sqlalchemy import func
router = APIRouter(
    prefix="/Applications",
    tags=['Applications']
)

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[int,Depends(current_user)]

class AddApplication(BaseModel):
    role_title : str
    status : Literal['applied','screening','interviewing','offer','rejected','withdrawn']
    job_url : str|None

    model_config = {
            'json_schema_extra': {
                'example':{
                    'role_title' : 'SDE',
                    'status': 'applied',
                    'job_url': ''
                }
            }
        }

class UpdateApplication(BaseModel):
    role_title : str
    status : Literal['applied','screening','interviewing','offer','rejected','withdrawn']
    job_url : str|None = None
    company_name : str|None = None

    model_config = {
            'json_schema_extra': {
                'example':{
                    'role_title' : 'Senior SDE',
                    'status': 'interviewing',
                    'job_url': 'https://example.com/job',
                    'company_name': 'Acme Corp'
                }
            }
        }

class PatchApplication(BaseModel):
    role_title : str|None = None
    status : Literal['applied','screening','interviewing','offer','rejected','withdrawn']|None = None
    job_url : str|None = None
    company_name : str|None = None

    model_config = {
            'json_schema_extra': {
                'example':{
                    'status': 'offer',
                    'job_url': 'https://example.com/updated',
                }
            }
        }

@router.post("/applications/",status_code=status.HTTP_201_CREATED)
async def add_new_application(db: db_dependency,application : AddApplication,user: user_dependency,company_name: str):
    company_detail = db.query(Companies).filter(
        func.lower(Companies.company_name) == company_name.lower(),
        Companies.user_id == user
    ).first()
    if company_detail is None:
        raise HTTPException(status_code=404,detail="enter valid company name")

    new_application = Applications(
        user_id = user,
        comapany_id = company_detail.company_id,
        role_title = application.role_title,
        status = application.status,
        applied_date = date.today(),
        job_url = application.job_url
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application

@router.get("/applications/",status_code=status.HTTP_200_OK)
async def get_all_applications(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    applications = db.query(Applications).filter(Applications.user_id == user).all()
    if not applications:
        return {"detail": "No applications found for the user"}

    return applications

@router.get("/applications/{application_id}",status_code=status.HTTP_200_OK)
async def get_application_by_id(application_id: int, db: db_dependency, user: user_dependency):
    application = db.query(Applications).filter(
        Applications.application_id == application_id,
        Applications.user_id == user
    ).first()
    if application is None:
        raise HTTPException(status_code=404, detail="application not found")
    return application

@router.put("/applications/{application_id}",status_code=status.HTTP_202_ACCEPTED)
async def update_application_by_id(application_id: int, db: db_dependency, user: user_dependency, updated: UpdateApplication):
    application = db.query(Applications).filter(
        Applications.application_id == application_id,
        Applications.user_id == user
    ).first()
    if application is None:
        raise HTTPException(status_code=404, detail="application not found")

    if updated.company_name is not None:
        company_detail = db.query(Companies).filter(
            func.lower(Companies.company_name) == updated.company_name.lower(),
            Companies.user_id == user
        ).first()
        if company_detail is None:
            raise HTTPException(status_code=404, detail="company not found")
        application.comapany_id = company_detail.company_id

    application.role_title = updated.role_title
    application.status = updated.status
    application.job_url = updated.job_url

    db.commit()
    db.refresh(application)
    return application

@router.delete("/applications/{application_id}",status_code=status.HTTP_200_OK)
async def delete_application_by_id(application_id: int, db: db_dependency, user: user_dependency):
    application = db.query(Applications).filter(
        Applications.application_id == application_id,
        Applications.user_id == user
    ).first()
    if application is None:
        raise HTTPException(status_code=404, detail="application not found")
    db.delete(application)
    db.commit()
    return {"detail": "application deleted"}

@router.patch("/applications/{application_id}",status_code=status.HTTP_200_OK)
async def patch_an_application_small_change(application_id: int, db: db_dependency, user: user_dependency, changes: PatchApplication):
    application = db.query(Applications).filter(
        Applications.application_id == application_id,
        Applications.user_id == user
    ).first()
    if application is None:
        raise HTTPException(status_code=404, detail="application not found")

    if changes.company_name is not None:
        company_detail = db.query(Companies).filter(
            func.lower(Companies.company_name) == changes.company_name.lower(),
            Companies.user_id == user
        ).first()
        if company_detail is None:
            raise HTTPException(status_code=404, detail="company not found")
        application.comapany_id = company_detail.company_id

    if changes.role_title is not None:
        application.role_title = changes.role_title
    if changes.status is not None:
        application.status = changes.status
    if changes.job_url is not None:
        application.job_url = changes.job_url

    db.commit()
    db.refresh(application)
    return application