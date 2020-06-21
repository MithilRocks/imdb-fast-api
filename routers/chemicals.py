from fastapi import APIRouter, HTTPException
import crud, schemas
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Chemical)
async def create_chemical(chemical: schemas.ChemicalCreate):
    db_chem = await crud.get_by_chemical_name(chemical.name)
    if db_chem:
        raise HTTPException(status_code=400, detail="chemical already created")
    return await crud.create_chemical(chemical=chemical)

# Get all chemicals by id
@router.get("/{chemical_id}", response_model=schemas.Chemical)
async def read_chemical(chemical_id: int):
    db_chem = await crud.get_chemical(chemical_id)
    if db_chem is None:
        raise HTTPException(status_code=400, detail="chemical not existing")
    return db_chem

# Get all chemicals
@router.get("/all", response_model=List[schemas.Chemical])
async def get_chemicals():
    return await crud.get_chemicals()