from fastapi import APIRouter,Depends,HTTPException,Request
from starlette import status
from models import Applications,Companies
from database import get_db
from sqlalchemy.orm import Session
from Routers.Auth import current_user
from pydantic import BaseModel,Field
from datetime import date
from typing import Annotated,Literal,List
from sqlalchemy import func
from slowapi.util import get_remote_address
from slowapi import Limiter
router = APIRouter(
    prefix="/Applications",
    tags=['Applications']
)
limiter = Limiter(key_func=get_remote_address)
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[int,Depends(current_user)]

class ApplicationCreate(BaseModel):
    role_title : str
    status : Literal['applied','screening','interviewing','offer','rejected','withdrawn']
    job_url : str|None = None
    notes: str | None = Field(default=None, max_length=1000)

    model_config = {
            'json_schema_extra': {
                'example':{
                    'role_title' : 'SDE',
                    'status': 'applied',
                    'job_url': '',
                    'notes' : ''
                }
            }
        }

class ApplicationUpdate(BaseModel):
    role_title : str
    status : Literal['applied','screening','interviewing','offer','rejected','withdrawn']
    job_url : str|None = None
    company_name : str|None = None
    notes: str | None = Field(default=None, max_length=1000)

    model_config = {
            'json_schema_extra': {
                'example':{
                    'role_title' : 'Senior SDE',
                    'status': 'interviewing',
                    'job_url': 'https://example.com/job',
                    'company_name': 'Acme Corp',
                    'notes' : 'a small note.'
                }
            }
        }

class ApplicationPatch(BaseModel):
    role_title : str|None = None
    status : Literal['applied','screening','interviewing','offer','rejected','withdrawn']|None = None
    job_url : str|None = None
    company_name : str|None = None
    notes: str | None = Field(default=None, max_length=1000)

    model_config = {
            'json_schema_extra': {
                'example':{
                    'status': 'offer',
                    'job_url': 'https://example.com/updated',
                    'notes':'small patch.'
                }
            }
        }

class ApplicationOut(BaseModel):
    application_id: int
    user_id: int
    comapany_id: int
    company_name : str|None = None
    role_title: str
    status: Literal['applied','screening','interviewing','offer','rejected','withdrawn']
    applied_date: date
    job_url: str|None = None
    notes: str | None = Field(default=None, max_length=1000)

    model_config = {
        'from_attributes': True,
        'json_schema_extra': {
            'example': {
                'application_id': 1,
                'user_id': 1,
                'comapany_id': 2,
                'company_name':'Google',
                'role_title': 'SDE',
                'status': 'applied',
                'applied_date': '2026-07-31',
                'job_url': 'https://example.com/job',
                'notes':'small patch.'
            }
        }
    }

def to_application_out(application: Applications, db: Session) -> ApplicationOut:
    out = ApplicationOut.model_validate(application)
    company = db.query(Companies).filter(Companies.company_id == application.comapany_id).first()
    out.company_name = company.company_name if company else None
    return out

@router.post("/applications/", status_code=status.HTTP_201_CREATED, response_model=ApplicationOut)
@limiter.limit("30/minute")
async def add_new_application(request: Request,db: db_dependency, application: ApplicationCreate, user: user_dependency, company_name: str):
    company_detail = db.query(Companies).filter(
        func.lower(Companies.company_name) == company_name.lower(),
        Companies.user_id == user
    ).first()
    if company_detail is None:
        raise HTTPException(status_code=404, detail="enter valid company name")

    new_application = Applications(
        user_id=user,
        comapany_id=company_detail.company_id,
        role_title=application.role_title,
        status=application.status,
        applied_date=date.today(),
        job_url=application.job_url,
        notes=application.notes
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return to_application_out(new_application, db)


@router.get("/applications/", status_code=status.HTTP_200_OK, response_model=List[ApplicationOut])
@limiter.limit("30/minute")
async def get_all_applications(request: Request,db: db_dependency, user: user_dependency, skip: int = 0, limit: int = 10):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    applications = db.query(Applications).filter(Applications.user_id == user)
    applications = applications.offset(skip).limit(limit).all()
    if not applications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No applications found for the user")

    return [to_application_out(application, db) for application in applications]


@router.get("/applications/{application_id}", status_code=status.HTTP_200_OK, response_model=ApplicationOut)
@limiter.limit("30/minute")
async def get_application_by_id(request: Request,application_id: int, db: db_dependency, user: user_dependency):
    application = db.query(Applications).filter(
        Applications.application_id == application_id,
        Applications.user_id == user
    ).first()
    if application is None:
        raise HTTPException(status_code=404, detail="application not found")
    return to_application_out(application, db)


@router.put("/applications/{application_id}", status_code=status.HTTP_202_ACCEPTED, response_model=ApplicationOut)
@limiter.limit("30/minute")
async def update_application_by_id(request: Request,application_id: int, db: db_dependency, user: user_dependency, updated: ApplicationUpdate):
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
    application.notes = updated.notes

    db.commit()
    db.refresh(application)
    return to_application_out(application, db)


@router.patch("/applications/{application_id}", status_code=status.HTTP_200_OK, response_model=ApplicationOut)
@limiter.limit("30/minute")
async def patch_an_application_small_change(request: Request,application_id: int, db: db_dependency, user: user_dependency, changes: ApplicationPatch):
    application = db.query(Applications).filter(Applications.application_id == application_id, Applications.user_id == user).first()
    if application is None:
        raise HTTPException(status_code=404, detail="application not found")

    if changes.company_name is not None:
        company_detail = db.query(Companies).filter(func.lower(Companies.company_name) == changes.company_name.lower(), Companies.user_id == user).first()
        if company_detail is None:
            raise HTTPException(status_code=404, detail="company not found")
        application.comapany_id = company_detail.company_id

    if changes.role_title is not None:
        application.role_title = changes.role_title
    if changes.status is not None:
        application.status = changes.status
    if changes.job_url is not None:
        application.job_url = changes.job_url
    if "notes" in changes.model_fields_set:
        application.notes = changes.notes

    db.commit()
    db.refresh(application)
    return to_application_out(application, db)


@router.delete("/applications/{application_id}",status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
async def delete_application_by_id(request: Request,application_id: int, db: db_dependency, user: user_dependency):
    application = db.query(Applications).filter(Applications.application_id == application_id,Applications.user_id == user).first()
    if application is None:
        raise HTTPException(status_code=404, detail="application not found")
    db.delete(application)
    db.commit()
    return {"detail": "application deleted"}