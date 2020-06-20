# import uvicorn
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, schemas, models
from database import SessionLocal, engine, database

import asyncio

models.Base.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/chemical/", response_model=schemas.Chemical)
async def create_chemical(chemical: schemas.ChemicalCreate):
    db_chem = await crud.get_by_chemical_name(chemical.name)
    if db_chem:
        raise HTTPException(status_code=400, detail="chemical already created")
    return await crud.create_chemical(chemical=chemical)

# Get all chemicals by id
@app.get("/chemical/{chemical_id}", response_model=schemas.Chemical)
async def read_chemical(chemical_id: int):
    db_chem = await crud.get_chemical(chemical_id)
    if db_chem is None:
        raise HTTPException(status_code=400, detail="chemical not existing")
    return db_chem

# Get all chemicals
@app.get("/chemicals", response_model=List[schemas.Chemical])
async def get_chemicals():
    return await crud.get_chemicals()

@app.get("/commodity/{id}")
async def get_commodity(id: int):
    db_comm = await crud.get_commodity(id)
    if db_comm is None:
        raise HTTPException(status_code=400, detail="commodity not found")
    db_chem = await crud.get_comm_chemicals(id)
    return {**db_comm, "chemical_composition":db_chem}

# Create a commodity
@app.post("/commodity/")
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

@app.put("/commodity/")
async def update_commodity(commodity: schemas.CommodityBase):
    db_com = await crud.get_by_commodity_name(commodity.name)
    if db_com is None:
        raise HTTPException(status_code=400, detail="commodity not found")
    return await crud.update_commodity(commodity)

@app.post("/add_chemical/")
async def add_chemical_to_commodity(commodity_id: int, chemical: schemas.ChemicalCommodityRel):
    db_chem = await crud.get_chemical(chemical.chemical_id)
    if db_chem is None:
        raise HTTPException(status_code=400, detail="chemical doesn't exist")
    
    db_comm = await crud.get_commodity(commodity_id)
    if db_comm is None:
        raise HTTPException(status_code=400, detail="commodity doesn't exist")

    return await crud.add_chemical(commodity_id=commodity_id, chemical=chemical)
    
""" if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True) """