from fastapi import APIRouter,Depends,Path
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from models import Users
from pydantic import BaseModel
from datetime import datetime
from utils import hash_password
router = APIRouter(
    prefix="/Auth",
    tags=['Auth']
)

class EnterUserData(BaseModel):
    id : int
    email : str
    hashed_password : str
    created_at : datetime

    model_config = {
        "json_schema_extra":{
            "example": {
                "id": 0,
                "email": "string",
                "hashed_password": "string",
                "created_at" : datetime.now()
            }
        }
    }



db_dependency = Annotated[Session,Depends(get_db)]

@router.post("/auth/registering new user")
async def register_new_user(db : db_dependency,user: EnterUserData):
    register_new_user_model = Users(
        id = user.id,
        email = user.email,
        hashed_password = hash_password(user.hashed_password),
        created_at = datetime.now()
    )
    db.add(register_new_user_model)
    db.commit()
    db.refresh(register_new_user_model)

    return {'ok':'added'}

@router.post("/auth/login")
async def login(): pass

@router.get("/auth/me/{id}")
async def get_current_user(db : db_dependency,id: int = Path(ge=0)): 
    user_data = db.query(Users).filter(Users.id == id).first()
    return user_data

    