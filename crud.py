from sqlalchemy.orm import Session
from database import database
import models, schemas

async def get_user(username: str):
    return await database.fetch_one(query=models.users.select().where(models.users.c.username == username))

async def get_by_element_name(name: str):
    return await database.fetch_one(query=models.elements.select().where(models.elements.c.name == name))

async def get_element(element_id: int):
    return await database.fetch_one(query=models.elements.select().where(models.elements.c.id == element_id))

async def get_elements():
    return await database.fetch_all(models.elements.select())

async def create_element(element: schemas.ElementCreate):
    element_c = models.elements.insert().values(**element.dict())
    pk = await database.execute(element_c)
    return {**element.dict(), "id":pk}

async def get_commodity(commodity_id: int):
    return await database.fetch_one(query=models.commodities.select().where(models.commodities.c.id == commodity_id))

async def get_comm_elements(commodity_id: int):
    elements = await database.fetch_all(query=models.relationships.select().where(models.relationships.c.commodity_id == commodity_id))
    final_elements = []
    for element in elements:
        final_elements.append(dict(element))
    return final_elements

async def get_comm_elements_formatted(commodity_id: int):
    async def element_composition(elements: models.ElementCommodityRelation):
        for element in elements:
            chem = await get_element(element.element_id)
            yield {"element":chem, "percentage":element.percentage}

    chem_comp = []
    comm_chem = await database.fetch_all(query=models.relationships.select().where(models.relationships.c.commodity_id == commodity_id))
    async for i in element_composition(comm_chem):
        chem_comp.append(i)
    return chem_comp

async def get_comm_element(commodity_id: int, element_id: int):
    return await database.fetch_one(query=models.relationships.select().where((models.relationships.c.commodity_id == commodity_id) & (models.relationships.c.element_id == element_id)))

async def get_by_commodity_name(name: str):
    return await database.fetch_one(query=models.commodities.select().where(models.commodities.c.name == name))

async def update_commodity(commodity: schemas.Commodity):
    await database.execute(models.commodities.update().values(**commodity.dict(exclude_unset=True)).where(models.commodities.c.id == commodity.id))
    return {**commodity.dict(exclude_unset=True)}

async def create_commodity(commodity: schemas.CommodityCreate):
    commodity_c = models.commodities.insert().values(**commodity.dict())
    pk = await database.execute(commodity_c)
    return {**commodity.dict(), "id":pk}

async def add_element(commodity_id: int, element: schemas.ElementCommodityRel):
    add_chem = models.relationships.insert({"element_id":element.element_id, "commodity_id":commodity_id, "percentage":element.percentage})
    pk = await database.execute(add_chem)
    return {"commodity_id":commodity_id, **element.dict(), "id":pk}

async def update_comm_element(chem_vals, unk_vals):
    query = "START TRANSACTION; \
        INSERT INTO elementcommodityrelation (id, element_id, commodity_id, percentage) VALUES (:id, :element_id, :commodity_id, :percentage) \
        ON duplicate KEY UPDATE percentage=VALUES(percentage); \
        DELETE FROM elementcommodityrelation WHERE percentage = 0;\
        COMMIT;"
    values = [chem_vals, unk_vals]
    return await database.execute_many(query=query, values=values)

async def delete_comm_element(commodity_id: int, element_id: int):
    return await database.fetch_one(query=models.relationships.delete().where((models.relationships.c.commodity_id == commodity_id) & (models.relationships.c.element_id == element_id)))
