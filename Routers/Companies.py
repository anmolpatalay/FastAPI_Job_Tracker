from fastapi import APIRouter,Path
from starlette import status
router = APIRouter(
    prefix="/Companies",
    tags=['Companies']
)

@router.post("/company",status_code=status.HTTP_201_CREATED)
async def add_new_company(): pass

@router.get("/company/get_all",status_code=status.HTTP_200_OK)
async def get_company_details(): pass

@router.get("/company_by_id/{id}",status_code=status.HTTP_200_OK)
async def get_company_by_id(id = Path(ge=0,le=100)) : pass

@router.put("/company_detail_update/{id}",status_code=status.HTTP_202_ACCEPTED)
async def update_company_detail(id = Path(ge=0,le=100)): pass

@router.delete("/company_deleted/{id}",status_code=status.HTTP_200_OK)
async def delete_a_company(id = Path(ge=0,le=100)) : pass
