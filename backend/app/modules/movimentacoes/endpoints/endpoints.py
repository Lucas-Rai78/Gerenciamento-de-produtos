from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.modules.movimentacoes.schemas import schemas
from app.modules.movimentacoes.service import service as movimentacao_service

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])


@router.post("", response_model=schemas.MovimentacaoResponse, status_code=status.HTTP_201_CREATED)
def registrar_movimentacao(mov: schemas.MovimentacaoCreate, db: Session = Depends(get_db)):
    return movimentacao_service.create_movimentacao(db=db, mov=mov)


@router.get("", response_model=List[schemas.MovimentacaoResponse])
def listar_movimentacoes(db: Session = Depends(get_db)):
    return movimentacao_service.get_movimentacoes(db=db)