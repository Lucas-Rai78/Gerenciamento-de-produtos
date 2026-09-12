from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.modules.produto.schemas import schemas
from app.modules.produto.service import service as produto_service

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("", response_model=schemas.ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return produto_service.create_produto(db=db, produto=produto)


@router.get("", response_model=List[schemas.ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return produto_service.get_produtos(db=db)


@router.get("/{produto_id}", response_model=schemas.ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    return produto_service.get_produto_by_id(db=db, produto_id=produto_id)


@router.put("/{produto_id}", response_model=schemas.ProdutoResponse)
def atualizar_produto(produto_id: int, dados: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return produto_service.update_produto(db=db, produto_id=produto_id, dados=dados)


@router.delete("/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    return produto_service.delete_produto(db=db, produto_id=produto_id)