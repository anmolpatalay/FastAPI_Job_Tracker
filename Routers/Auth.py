from fastapi import APIRouter,Depends,Path,HTTPException,status
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from models import Users
from pydantic import BaseModel,EmailStr,Field,StringConstraints,field_validator,ConfigDict
from datetime import datetime,timedelta,timezone
from utils import hash_password,bcrypt_context
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from dotenv import load_dotenv
import os
import re
router = APIRouter(
    prefix="/Auth",
    tags=['Auth']
)

class EnterUserData(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r"[@$!%*?&#]", value):
            raise ValueError("Password must contain at least one special character")

        return value



    model_config = {
        "json_schema_extra":{
            "example": {
                "email": "string",
                "password": "string",
            }
        }
    }

class EnterPassword(BaseModel):
    old_password : str
    new_password: str

class PasswordOut(BaseModel):
    new_password: str
#################################### Access_Token ####################################
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # pydantic v2; use `orm_mode=True` in v1
    id: int
    email: str
    created_at: datetime | None = None

def create_token(email:str,user_id:int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub" : email,
        "id" : user_id,
        "exp": expire
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


def create_refresh_token(email,user_id):
    expire = datetime.now(timezone.utc)+timedelta(days=2)
    payload = {
        "sub":email,
        "id":user_id,
        "exp": expire,
        "type": "refresh"
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Auth/login")
auth_dependency = Depends(oauth2_scheme)
#################################### END POINTS ####################################
db_dependency = Annotated[Session,Depends(get_db)]

# create a sepertae function. you cannot use get_current_user at the last of this code because it is a endpoint. you must use a function in your dependency
async def current_user(db : db_dependency,user: str = auth_dependency): 
    try:
        payload = jwt.decode(user,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    email = payload.get('sub')  # decode the payload first very important
    user_id = payload.get('id')
    return user_id



@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register_new_user(db : db_dependency,user: EnterUserData):
    if db.query(Users).filter(Users.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already exists")
    register_new_user_model = Users(
        email = user.email,
        hashed_password = hash_password(user.password),
        created_at = datetime.now()
    )
    db.add(register_new_user_model)
    db.commit()
    db.refresh(register_new_user_model)

@router.post("/login")
async def login(db: db_dependency,form_data : OAuth2PasswordRequestForm = Depends()): 
    email_id = form_data.username
    password1 = form_data.password
    user_detail = db.query(Users).filter(Users.email == email_id).first()
    if user_detail is None:
        return {"user":"username not available"}
    if bcrypt_context.verify(password1,user_detail.hashed_password):
        access_token = create_token(email=user_detail.email, user_id=user_detail.id)
        refresh_token = create_refresh_token(email=user_detail.email, user_id=user_detail.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(status_code=401,detail="Invalid Credentials")


@router.get("/me")
async def get_current_user(user: str = auth_dependency): 
    try:
        payload = jwt.decode(user,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    email = payload.get('sub')
    user_id = payload.get('id')
    return user_id


@router.get("/all", response_model=list[UserOut])
async def get_all(db: db_dependency, user: str = auth_dependency):
    try:
        payload = jwt.decode(user, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    email = payload.get('sub')
    if email.split("@")[0] == "admin":
        return db.query(Users).all()
    return [db.query(Users).filter(Users.email == email).first()]

@router.put("/reset_password",status_code=status.HTTP_202_ACCEPTED,response_model= PasswordOut)
async def reset_password(
    db: db_dependency,
    password_data: EnterPassword,
    user_id: int = Depends(current_user),
):
    user_info = db.query(Users).filter(Users.id == user_id).first()
    if user_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not bcrypt_context.verify(password_data.old_password, user_info.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Old password is incorrect")

    user_info.hashed_password = hash_password(password_data.new_password)
    db.commit()
    db.refresh(user_info)

    return PasswordOut(new_password=password_data.new_password)

@router.post("/refresh")
async def refresh(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token") from exc

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token type")

    access_token = create_token(payload["sub"], payload["id"])
    new_refresh_token = create_refresh_token(payload["sub"], payload["id"])

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }