from fastapi import APIRouter,Depends,HTTPException
from starlette import status
from models import Applications,Companies
from database import get_db
from sqlalchemy.orm import Session
from Routers.Auth import current_user
from pydantic import BaseModel
from datetime import date
from typing import Annotated,Literal
from Routers.Auth import current_user
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

@router.post("/applications/",status_code=status.HTTP_201_CREATED)
async def add_new_application(db: db_dependency,application : AddApplication,user: user_dependency,company_name: str):

    company_detail = db.query(Companies).filter(func.lower(Companies.company_name) == company_name.lower()).first()
    print(company_detail)
    print(company_detail.company_id)
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
    



@router.get("/applications/",status_code=status.HTTP_200_OK)
async def get_all_applications(): pass

@router.get("/applications/",status_code=status.HTTP_200_OK)
async def get_application_by_id(): pass

@router.put("/applications/",status_code=status.HTTP_201_CREATED)
async def update_application_by_id(): pass

@router.delete("/applications/",status_code=status.HTTP_200_OK)
async def delete_application_by_id(): pass

@router.patch("/applications/",status_code=status.HTTP_201_CREATED)
async def patch_an_application_small_change(): pass