from typing import List
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.orm import Session

import crud, schemas, models
from database import SessionLocal, engine, database

from routers import elements, commodities

models.Base.metadata.create_all(engine)

app = FastAPI()

security = HTTPBasic()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

def fake_hash_password(password: str):
    return "hashed" + password

async def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    user = await crud.get_user(credentials.username)
    correct_username = secrets.compare_digest(credentials.username, user.username)
    correct_password = secrets.compare_digest(fake_hash_password(credentials.password), user.password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

app.include_router(
    elements.router,
    prefix="/element",
    responses={404: {"description":"api not found"}},
    dependencies=[Depends(get_current_username)]
)

app.include_router(
    commodities.router,
    prefix="/commodity",
    responses={404: {"description":"api not found"}},
    dependencies=[Depends(get_current_username)]
)