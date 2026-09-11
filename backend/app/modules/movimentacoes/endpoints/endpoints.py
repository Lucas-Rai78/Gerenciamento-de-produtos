from fastapi import FastAPI, Depends, status, app
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database.database import engine, get_db
from app.modules.models import models
from app.modules.schemas import schemas
from app.modules.service import crud

@app.post("/movimentacoes", response_model=schemas.MovimentacaoResponse, status_code=status.HTTP_201_CREATED)
def registrar_movimentacao(mov: schemas.MovimentacaoCreate, db: Session = Depends(get_db)):
    return crud.create_movimentacao(db=db, mov=mov)

@app.get("/movimentacoes", response_model=List[schemas.MovimentacaoResponse])
def listar_movimentacoes(db: Session = Depends(get_db)):
    return crud.get_movimentacoes(db=db)