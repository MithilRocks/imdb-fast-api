from fastapi import APIRouter, HTTPException
import crud, schemas
from typing import List

router = APIRouter()

@router.get("/{id}")
async def get_commodity(id: int):
    db_comm = await crud.get_commodity(id)
    if db_comm is None:
        raise HTTPException(status_code=400, detail="commodity not found")
    db_chem = await crud.get_comm_chemicals(id)
    return {**db_comm, "chemical_composition":db_chem}

# Create a commodity
@router.post("/")
async def create_commodity(commodity: schemas.CommodityCreate):
    db_comm = await crud.get_by_commodity_name(commodity.name)
    if db_comm:
        raise HTTPException(status_code=400, detail="commodity already exists")

    db_chem = await crud.get_by_chemical_name('unknown')
    if db_chem is None:
        db_chem = await crud.create_chemical(chemical=schemas.ChemicalCreate(name='unknown'))
    
    add_comm = await crud.create_commodity(commodity=commodity)
    await crud.add_chemical(commodity_id=add_comm['id'], chemical=schemas.ChemicalCommodityRel(chemical_id=db_chem['id'],percentage=100))
    return {**add_comm, "chemical_composition":[{"element":db_chem, "percentage":100}]}

@router.put("/")
async def update_commodity(commodity: schemas.CommodityBase):
    db_com = await crud.get_by_commodity_name(commodity.name)
    if db_com is None:
        raise HTTPException(status_code=400, detail="commodity not found")
    return await crud.update_commodity(commodity)

@router.post("/add_chemical")
async def add_chemical_to_commodity(commodity_id: int, chemical: schemas.ChemicalCommodityRel):
    db_chem = await crud.get_chemical(chemical.chemical_id)
    if db_chem is None:
        raise HTTPException(status_code=400, detail="chemical doesn't exist")
    
    db_comm = await crud.get_commodity(commodity_id)
    if db_comm is None:
        raise HTTPException(status_code=400, detail="commodity doesn't exist")

    return await crud.add_chemical(commodity_id=commodity_id, chemical=chemical)