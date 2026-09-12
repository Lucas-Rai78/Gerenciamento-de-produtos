from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.produto.models import models
from app.modules.produto.schemas import schemas
from app.modules.produto.repository import produto as produto_repository


def get_produtos(db: Session):
    return produto_repository.get_produtos(db)


def get_produto_by_id(db: Session, produto_id: int):
    produto = produto_repository.get_produto_by_id(db, produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado."
        )
    return produto


def create_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(**produto.model_dump())
    return produto_repository.create_produto(db, db_produto)


def update_produto(db: Session, produto_id: int, dados: schemas.ProdutoCreate):
    db_produto = get_produto_by_id(db, produto_id)
    return produto_repository.update_produto(db, db_produto, dados.model_dump())


def delete_produto(db: Session, produto_id: int):
    db_produto = get_produto_by_id(db, produto_id)
    return produto_repository.delete_produto(db, db_produto)