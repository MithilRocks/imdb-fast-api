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
    
    def find_chem_per(chems, id):
        for chem in chems:
            if chem['chemical_id'] == id:
                return chem

    db_chem = await crud.get_chemical(chemical.chemical_id)
    if db_chem is None:
        raise HTTPException(status_code=400, detail="chemical doesn't exist")
    
    db_comm = await crud.get_commodity(commodity_id)
    if db_comm is None:
        raise HTTPException(status_code=400, detail="commodity doesn't exist")

    db_chems = await crud.get_comm_chemicals(commodity_id)

    unknown = await crud.get_by_chemical_name('unknown')
    unknown_rel = find_chem_per(db_chems, unknown['id'])
    if unknown_rel['percentage'] == 0:
        raise HTTPException(status_code=400, detail="unable to add chemical; please remove a chemical to add a new one")

    chemical_rel = find_chem_per(db_chems, chemical.chemical_id)

    if chemical.percentage <= unknown_rel['percentage']:
        
        if chemical_rel:
            new_chem_per = chemical_rel['percentage'] + chemical.percentage
        else:
            new_chem_per = chemical.percentage
        
        new_unk_per = unknown_rel['percentage'] - chemical.percentage
        unknown_rel['percentage'], chemical_rel['percentage'] = new_unk_per, new_chem_per

        up_chem = await crud.update_comm_chemical(chemical_rel, unknown_rel)
    else:
        raise HTTPException(status_code=400, detail="unable to add chemical; please remove a chemical to add a new one")
    
    return {**db_comm, "chemical_composition":db_chems}

@router.delete("/delete_chemical")
async def delete_chemical_from_commodity(commodity_id: int, chemical_id: int):

    db_chem = await crud.get_chemical(chemical_id)
    if db_chem is None:
        raise HTTPException(status_code=400, detail="chemical doesn't exist")
    
    db_comm = await crud.get_commodity(commodity_id)
    if db_comm is None:
        raise HTTPException(status_code=400, detail="commodity doesn't exist")

    db_chems = await crud.get_comm_chemicals(commodity_id)
    del_chem = await crud.delete_comm_chemical(commodity_id, chemical_id)
    
    if del_chem:
        pass
    else:
        return HTTPException(status_code=400, detail="this chemical is not in the commodity")
