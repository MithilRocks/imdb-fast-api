from fastapi import APIRouter, HTTPException
import crud, schemas
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Element, tags=['Creation Endpoints'])
async def create_element(element: schemas.ElementCreate):
    db_chem = await crud.get_by_element_name(element.name)
    if db_chem:
        raise HTTPException(status_code=400, detail="element already created")
    return await crud.create_element(element=element)

# Get all elements
@router.get("/all", response_model=List[schemas.Element], tags=['Main Task Endpoints'])
async def get_elements():
    return await crud.get_elements()

