from fastapi import APIRouter,Path,Depends,HTTPException,Query
from starlette import status
from Routers.Auth import current_user
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from database import get_db
from typing import Annotated
from models import Companies
router = APIRouter(
    prefix="/Companies",
    tags=['Companies']
)
db_dependency = Annotated[Session,Depends(get_db)]
current_user_dependency = Annotated[int,Depends(current_user)]

class AddCompany(BaseModel):

    company_name : str
    note : str

    model_config = {
           "json_schema_extra":{
               "example": {
                   "company_name": "string",
                   "note": "string",
               }
           }
       }


@router.post("/company",status_code=status.HTTP_201_CREATED)
async def add_new_company(db: db_dependency, user :current_user_dependency,company : AddCompany = None):
    if user is None:
        raise HTTPException(status_code=404,detail="User not found/auntenticated")
    
    company_model = Companies(
        user_id = user,
        company_name = company.company_name,
        note = company.note
    )
    db.add(company_model)
    db.commit()
    db.refresh(company_model)

@router.get("/company/get_all",status_code=status.HTTP_200_OK)
async def get_company_details(db: db_dependency, user :current_user_dependency): 
    companies = db.query(Companies).filter(Companies.user_id == user).all()
    return companies

@router.get("/company_by_id/",status_code=status.HTTP_200_OK)  # if you put id before db dependency as a query parameter, it wont work. if you want to keep id before db dependeny in the path parameter
async def get_company_by_id(db: db_dependency, user :current_user_dependency,id :int =Query(ge=0,le=100)) : 
    if user is None:
        raise HTTPException(status_code=404,detail="user not found")
    company = db.query(Companies).filter(Companies.company_id == id, Companies.user_id ==user).first()
    if company is None:
        raise HTTPException(status_code=404,detail='company Not found')
    return company

@router.put("/company_detail_update/{id}",status_code=status.HTTP_202_ACCEPTED)
async def update_company_detail(id: int,db: db_dependency, user :current_user_dependency,updated_note: str,updated_company_name: str): 
    company_to_update = db.query(Companies).filter(Companies.company_id == id,Companies.user_id==user).first()
    if company_to_update is None:
        raise HTTPException(status_code=404,detail='company Not found')
    company_to_update.company_name = updated_company_name
    company_to_update.note = updated_note
    db.commit()
    db.refresh(company_to_update)

@router.delete("/company_deleted/",status_code=status.HTTP_200_OK)
async def delete_a_company(db: db_dependency,usr: current_user_dependency,id:int) :
    if usr is None:
        raise HTTPException(status_code=404,detail="user are not authenticated")  
    company_to_delete = db.query(Companies).filter(Companies.company_id == id,Companies.user_id == usr).first()
    if company_to_delete is None:
        raise HTTPException(status_code=404,detail="company not found")
    db.delete(company_to_delete)
    db.commit()
    
