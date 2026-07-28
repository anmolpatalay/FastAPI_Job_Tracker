from fastapi import APIRouter,Depends,Path
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from models import Users
from pydantic import BaseModel,EmailStr
from datetime import datetime,timedelta,timezone
from utils import hash_password,bcrypt_context
from jose import jwt
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
router = APIRouter(
    prefix="/Auth",
    tags=['Auth']
)

class EnterUserData(BaseModel):
    email : EmailStr
    password : str

    model_config = {
        "json_schema_extra":{
            "example": {
                "email": "string",
                "password": "string",
            }
        }
    }
#################################### Access_Token ####################################
SECRET_KEY = "DHIWEHF83YFWHFKJEBF3E0RU4390RUEDFNWEBFWEFlkheugerhfiuf98rfbfb8U0ihbhjbHVUUG88UBJVGCYTDFU879E7983289H34JBWJEOGUE89GEEVBEJVHEIYH"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(email:str,user_id:int):
    expire = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub" : email,
        "id" : user_id,
        "exp" : expire
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Auth/auth/login")
auth_dependency = Depends(oauth2_scheme)
#################################### END POINTS ####################################
db_dependency = Annotated[Session,Depends(get_db)]

@router.post("/auth/registering new user")
async def register_new_user(db : db_dependency,user: EnterUserData):
    register_new_user_model = Users(
        email = user.email,
        hashed_password = hash_password(user.password),
        created_at = datetime.now()
    )
    db.add(register_new_user_model)
    db.commit()
    db.refresh(register_new_user_model)

    return {'ok':'added'}

@router.post("/auth/login")
async def login(db: db_dependency,form_data : OAuth2PasswordRequestForm = Depends()): 
    email_id = form_data.username
    password1 = form_data.password
    print(email_id)
    print(password1)
    user_detail = db.query(Users).filter(Users.email == email_id).first()
    if user_detail is None:
        return {"user":"username not available"}
    if bcrypt_context.verify(password1,user_detail.hashed_password):
        token = create_token(email = user_detail.email,user_id=user_detail.id)
        return {"access_token": token, "token_type":'bearer'}
    else:
        return{"failed","not authenticated"}


@router.get("/auth/me/")
async def get_current_user(db : db_dependency,user: str = auth_dependency): 
    payload = jwt.decode(user,SECRET_KEY,algorithms=[ALGORITHM])
    user_detail = db.query(Users).filter(Users.id == payload["id"]).first()
    return user_detail.created_at,user_detail.email

    