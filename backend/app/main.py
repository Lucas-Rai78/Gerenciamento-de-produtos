from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database.database import engine, get_db
from app.modules.models import models
from app.modules.schemas import schemas
from app.modules.service import crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gerenciador de Estoque - LaPiazza")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

