from fastapi import APIRouter, HTTPException
import crud, schemas
from typing import List

router = APIRouter()

def find_chem(chems, id):
    for chem in chems:
        if chem['element_id'] == id:
            return chem

@router.get("/{id}", tags=['Main Task Endpoints'])
async def get_commodity(id: int):
    db_comm = await crud.get_commodity(id)
    if db_comm is None:
        raise HTTPException(status_code=400, detail="commodity not found")
    db_chem = await crud.get_comm_elements_formatted(id)
    return {**db_comm, "chemical_composition":db_chem}

# Create a commodity
@router.post("/")
async def create_commodity(commodity: schemas.CommodityCreate):
    db_comm = await crud.get_by_commodity_name(commodity.name)
    if db_comm:
        raise HTTPException(status_code=400, detail="commodity already exists")

    db_chem = await crud.get_by_element_name('unknown')
    if db_chem is None:
        db_chem = await crud.create_element(element=schemas.ElementCreate(name='unknown'))
    
    add_comm = await crud.create_commodity(commodity=commodity)
    await crud.add_element(commodity_id=add_comm['id'], element=schemas.ElementCommodityRel(element_id=db_chem['id'],percentage=100))
    return {**add_comm, "chemical_composition":[{"element":db_chem, "percentage":100}]}

@router.put("/", tags=['Main Task Endpoints'])
async def update_commodity(commodity: schemas.Commodity):
    db_com = await crud.get_by_commodity_name(commodity.name)
    if db_com is None:
        raise HTTPException(status_code=400, detail="commodity not found")
    return await crud.update_commodity(commodity)

@router.post("/add_element", tags=['Main Task Endpoints'])
async def add_element_to_commodity(commodity_id: int, element: schemas.ElementCommodityRel):

    db_chem = await crud.get_element(element.element_id)
    if db_chem is None:
        raise HTTPException(status_code=400, detail="element doesn't exist")
    
    db_comm = await crud.get_commodity(commodity_id)
    if db_comm is None:
        raise HTTPException(status_code=400, detail="commodity doesn't exist")

    db_chems = await crud.get_comm_elements(commodity_id)

    unknown = await crud.get_by_element_name('unknown')
    unknown_rel = find_chem(db_chems, unknown['id'])
    if unknown_rel is None:
        raise HTTPException(status_code=400, detail="unable to add element; please remove a element to add a new one")
    elif unknown['id'] == element.element_id:
        raise HTTPException(status_code=400, detail="unknown element cannot be added")

    element_rel = find_chem(db_chems, element.element_id)

    if element.percentage <= unknown_rel['percentage']:
        
        if element_rel:
            element_rel['percentage'] = element_rel['percentage'] + element.percentage
        else:
            element_rel = {**unknown_rel}
            element_rel['element_id'] = element.element_id
            element_rel['id'] = None
            element_rel['percentage'] = element.percentage
        
        new_unk_per = unknown_rel['percentage'] - element.percentage
        unknown_rel['percentage'] = new_unk_per

        up_chem = await crud.update_comm_element(element_rel, unknown_rel)
    else:
        raise HTTPException(status_code=400, detail="unable to add element; please remove a element to add a new one")
    
    db_chems = await crud.get_comm_elements_formatted(commodity_id)

    return {**db_comm, "chemical_composition":db_chems}

@router.delete("/delete_element", tags=['Main Task Endpoints'])
async def delete_element_from_commodity(commodity_id: int, element_id: int):

    db_comm = await crud.get_commodity(commodity_id)
    if db_comm is None:
        raise HTTPException(status_code=400, detail="commodity doesn't exist")

    db_chems = await crud.get_comm_elements(commodity_id)
    if list(filter(lambda x: x['element_id'] == element_id, db_chems)) == []:
        raise HTTPException(status_code=400, detail="element doesn't exist in commodity")

    unknown = await crud.get_by_element_name('unknown')
    if element_id == unknown['id']:
        raise HTTPException(status_code=400, detail="unknown element cannot be removed")

    unknown_rel = find_chem(db_chems, unknown['id'])
    element_rel = find_chem(db_chems, element_id)
    
    if unknown_rel is None:
        unknown_rel = {**element_rel}
        unknown_rel['element_id'] = unknown['id']
        unknown_rel['id'] = None
        unknown_rel['percentage'] = element_rel['percentage']
    else:
        unknown_rel['percentage']= (unknown_rel['percentage']+element_rel['percentage'])
    
    element_rel['percentage'] = 0
    
    up_chem = await crud.update_comm_element(element_rel, unknown_rel)

    db_chems = await crud.get_comm_elements_formatted(commodity_id)
    
    return {**db_comm, "chemical_composition":db_chems}
