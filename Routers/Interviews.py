from fastapi import APIRouter,Path
from starlette import status
router = APIRouter(
    prefix="/Interviews",
    tags=['Interviews']
)

@router.post("/interviews",status_code=status.HTTP_201_CREATED)
async def add_interview_details(): pass
