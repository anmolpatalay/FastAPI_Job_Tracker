from fastapi import APIRouter,Depends,HTTPException
from starlette import status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime
from database import get_db
from Routers.Auth import current_user
from models import Interviews, Applications

router = APIRouter(
    prefix="/Interviews",
    tags=['Interviews']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[int, Depends(current_user)]

class InterviewCreate(BaseModel):
    application_id: int
    round_name: str
    scheduled_at: datetime

    model_config = {
        'json_schema_extra': {
            'example': {
                'application_id': 1,
                'round_name': 'Phone Screen',
                'scheduled_at': '2026-08-01T15:30:00'
            }
        }
    }

class InterviewOut(BaseModel):
    interview_id: int
    application_id: int
    round_name: str
    scheduled_at: datetime

    model_config = {
        'from_attributes': True,
        'json_schema_extra': {
            'example': {
                'interview_id': 1,
                'application_id': 1,
                'round_name': 'Phone Screen',
                'scheduled_at': '2026-08-01T15:30:00'
            }
        }
    }

@router.post("/interviews", status_code=status.HTTP_201_CREATED, response_model=InterviewOut)
async def add_interview_details(interview: InterviewCreate, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    application = db.query(Applications).filter(
        Applications.application_id == interview.application_id,
        Applications.user_id == user
    ).first()
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    new_interview = Interviews(
        application_id=interview.application_id,
        round_name=interview.round_name,
        scheduled_at=interview.scheduled_at
    )
    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)
    return InterviewOut.model_validate(new_interview)
