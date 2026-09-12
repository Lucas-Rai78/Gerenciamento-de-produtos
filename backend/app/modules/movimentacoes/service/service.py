from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.movimentacoes.models import models
from app.modules.movimentacoes.schemas import schemas
from app.modules.movimentacoes.repository import movimentacoes as movimentacao_repository
from app.modules.produto.service import service as produto_service


def create_movimentacao(db: Session, mov: schemas.MovimentacaoCreate):
    produto = produto_service.get_produto_by_id(db, mov.produto_id)

    if mov.tipo == "saida":
        if produto.quantidadeEstoque < mov.quantidade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Estoque insuficiente para a saída. "
                    f"Disponível: {produto.quantidadeEstoque}, Solicitado: {mov.quantidade}"
                )
            )
        produto.quantidadeEstoque -= mov.quantidade

    elif mov.tipo == "entrada":
        produto.quantidadeEstoque += mov.quantidade

    db_mov = models.MovimentacaoProduto(**mov.model_dump())
    return movimentacao_repository.create_movimentacao(db, db_mov)


def get_movimentacoes(db: Session):
    return movimentacao_repository.get_movimentacoes(db)