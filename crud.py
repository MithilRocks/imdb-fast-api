from sqlalchemy.orm import Session
from database import database
import models, schemas

async def get_by_chemical_name(name: str):
    return await database.fetch_one(query=models.chemicals.select().where(models.chemicals.c.name == name))

async def get_chemical(chemical_id: int):
    return await database.fetch_one(query=models.chemicals.select().where(models.chemicals.c.id == chemical_id))

async def get_chemicals():
    return await database.fetch_all(models.chemicals.select())

async def create_chemical(chemical: schemas.ChemicalCreate):
    chemical_c = models.chemicals.insert().values(**chemical.dict())
    pk = await database.execute(chemical_c)
    return {**chemical.dict(), "id":pk}

async def get_commodity(commodity_id: int):
    return await database.fetch_one(query=models.commodities.select().where(models.commodities.c.id == commodity_id))

async def get_comm_chemicals(commodity_id: int):
    chemicals = await database.fetch_all(query=models.relationships.select().where(models.relationships.c.commodity_id == commodity_id))
    final_chemicals = []
    for chemical in chemicals:
        final_chemicals.append(dict(chemical))
    return final_chemicals

""" async def get_comm_chemicals(commodity_id: int):
    async def chemical_composition(chemicals: models.ChemicalCommodityRelation):
        for chemical in chemicals:
            chem = await get_chemical(chemical.chemical_id)
            yield {"element":chem, "percentage":chemical.percentage}

    chem_comp = []
    comm_chem = await database.fetch_all(query=models.relationships.select().where(models.relationships.c.commodity_id == commodity_id))
    async for i in chemical_composition(comm_chem):
        chem_comp.append(i)
    return chem_comp """

async def get_comm_chemical(commodity_id: int, chemical_id: int):
    return await database.fetch_one(query=models.relationships.select().where((models.relationships.c.commodity_id == commodity_id) & (models.relationships.c.chemical_id == chemical_id)))

async def get_by_commodity_name(name: str):
    return await database.fetch_one(query=models.commodities.select().where(models.commodities.c.name == name))

async def update_commodity(commodity: schemas.CommodityBase):
    await database.execute(models.commodities.update().values(**commodity.dict(exclude_unset=True)).where(models.commodities.c.name == commodity.name))
    return {**commodity.dict(exclude_unset=True)}

async def create_commodity(commodity: schemas.CommodityCreate):
    commodity_c = models.commodities.insert().values(**commodity.dict())
    pk = await database.execute(commodity_c)
    return {**commodity.dict(), "id":pk}

async def add_chemical(commodity_id: int, chemical: schemas.ChemicalCommodityRel):
    add_chem = models.relationships.insert({"chemical_id":chemical.chemical_id, "commodity_id":commodity_id, "percentage":chemical.percentage})
    pk = await database.execute(add_chem)
    return {"commodity_id":commodity_id, **chemical.dict(), "id":pk}

async def update_comm_chemical(chem_vals, unk_vals):
    query = "INSERT INTO chemicalcommodityrelation (id, chemical_id, commodity_id, percentage) VALUES (:id, :chemical_id, :commodity_id, :percentage) \
        ON duplicate KEY UPDATE percentage=VALUES(percentage)"
    values = [chem_vals, unk_vals]
    return await database.execute_many(query=query, values=values)

async def delete_comm_chemical(commodity_id: int, chemical_id: int):
    return await database.fetch_one(query=models.relationships.delete().where((models.relationships.c.commodity_id == commodity_id) & (models.relationships.c.chemical_id == chemical_id)))
