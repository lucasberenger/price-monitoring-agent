from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import create_db_and_tables
from app.routers import products

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  
    yield 

app = FastAPI(lifespan=lifespan)

app.include_router(products.router)
    
