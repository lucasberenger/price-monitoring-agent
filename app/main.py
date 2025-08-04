from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.db import create_db_and_tables
from .routers import products

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  
    yield 

app = FastAPI(lifespan=lifespan)

app.include_router(products.router)
    
