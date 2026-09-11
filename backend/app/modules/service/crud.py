from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.models import models
from app.modules.schemas import schemas

# --- PRODUTOS ---

def get_produtos(db: Session):
    return db.query(models.Produto).all()

def get_produto_by_id(db: Session, produto_id: int):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Produto com ID {produto_id} não encontrado."
        )
    return produto

def create_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def update_produto(db: Session, produto_id: int, dados: schemas.ProdutoCreate):
    db_produto = get_produto_by_id(db, produto_id)
    
    for chave, valor in dados.model_dump().items():
        setattr(db_produto, chave, valor)

    db.commit()
    db.refresh(db_produto)
    return db_produto

def delete_produto(db: Session, produto_id: int):
    db_produto = get_produto_by_id(db, produto_id)
    db.delete(db_produto)
    db.commit()
    return db_produto

# --- MOVIMENTAÇÕES ---

def create_movimentacao(db: Session, mov: schemas.MovimentacaoCreate):
    produto = get_produto_by_id(db, mov.produto_id)

    # Validação de Regra de Negócio: Estoque Insuficiente
    if mov.tipo == "saida":
        if produto.quantidadeEstoque < mov.quantidade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estoque insuficiente para a saída. Disponível: {produto.quantidadeEstoque}, Solicitado: {mov.quantidade}"
            )
        produto.quantidadeEstoque -= mov.quantidade

    elif mov.tipo == "entrada":
        produto.quantidadeEstoque += mov.quantidade

    db_mov = models.MovimentacaoProduto(**mov.model_dump())
    db.add(db_mov)
    db.commit()
    db.refresh(db_mov)
    return db_mov

def get_movimentacoes(db: Session):
    return db.query(models.MovimentacaoProduto).order_by(models.MovimentacaoProduto.id.desc()).all()