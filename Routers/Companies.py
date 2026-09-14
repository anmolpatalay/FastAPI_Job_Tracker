from fastapi import APIRouter,Path,Depends,HTTPException,Query
from starlette import status
from Routers.Auth import current_user
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from database import get_db
from typing import Annotated
from models import Companies

router = APIRouter(
    prefix="/companies",
    tags=['Companies']
)
db_dependency = Annotated[Session,Depends(get_db)]
current_user_dependency = Annotated[int,Depends(current_user)]

class CompanyCreate(BaseModel):
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

class CompanyOut(BaseModel):
    company_id: int
    user_id: int
    company_name: str
    note: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra":{
            "example": {
                "company_id": 1,
                "user_id": 1,
                "company_name": "Acme Corp",
                "note": "Important client"
            }
        }
    }

class CompanyUpdate(BaseModel):
    company_name: str
    note: str

    model_config = {
        "json_schema_extra":{
            "example": {
                "company_name": "Acme Corp",
                "note": "Updated note"
            }
        }
    }

@router.post("",status_code=status.HTTP_201_CREATED,response_model=CompanyOut)
async def add_new_company(db: db_dependency, user :current_user_dependency, company: CompanyCreate):
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
    return CompanyOut.model_validate(company_model)

@router.get("",status_code=status.HTTP_200_OK, response_model=list[CompanyOut])
async def get_company_details(
    db: db_dependency,
    user :current_user_dependency,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, gt=0, le=100)
): 
    companies = db.query(Companies).filter(Companies.user_id == user)
    companies = companies.offset(skip).limit(limit).all()
    return [CompanyOut.model_validate(company) for company in companies]

@router.get("/{company_id}",status_code=status.HTTP_200_OK, response_model=CompanyOut)
async def get_company_by_id(db: db_dependency, user :current_user_dependency, company_id: int = Path(ge=1)):
    if user is None:
        raise HTTPException(status_code=404,detail="user not found")
    company = db.query(Companies).filter(Companies.company_id == company_id, Companies.user_id ==user).first()
    if company is None:
        raise HTTPException(status_code=404,detail='company Not found')
    return CompanyOut.model_validate(company)

@router.put("/{company_id}",status_code=status.HTTP_202_ACCEPTED,response_model=CompanyOut)
async def update_company_detail(company_id: int, db: db_dependency, user :current_user_dependency, company: CompanyUpdate):
    company_to_update = db.query(Companies).filter(Companies.company_id == company_id,Companies.user_id==user).first()
    if company_to_update is None:
        raise HTTPException(status_code=404,detail='company Not found')
    company_to_update.company_name = company.company_name
    company_to_update.note = company.note
    db.commit()
    db.refresh(company_to_update)
    return CompanyOut.model_validate(company_to_update)

@router.delete("/{company_id}",status_code=status.HTTP_200_OK)
async def delete_a_company(db: db_dependency, usr: current_user_dependency, company_id: int = Path(ge=1)):
    if usr is None:
        raise HTTPException(status_code=404,detail="user are not authenticated")
    company_to_delete = db.query(Companies).filter(Companies.company_id == company_id,Companies.user_id == usr).first()
    if company_to_delete is None:
        raise HTTPException(status_code=404,detail="company not found")
    db.delete(company_to_delete)
    db.commit()
    return {"detail": "company deleted"}
    
