from fastapi import APIRouter
from starlette import status
router = APIRouter(
    prefix="/Applications",
    tags=['Applications']
)

@router.post("/applications/",status_code=status.HTTP_201_CREATED)
async def add_new_application(): pass

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