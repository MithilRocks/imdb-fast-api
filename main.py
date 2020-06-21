import uvicorn
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, schemas, models
from database import SessionLocal, engine, database

from routers import chemicals, commodities

models.Base.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(
    chemicals.router,
    prefix="/chemical",
    responses={404: {"description":"api not found"}}
)

app.include_router(
    commodities.router,
    prefix="/commodity",
    responses={404: {"description":"api not found"}}
)
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)