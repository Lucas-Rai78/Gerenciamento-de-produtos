from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import schemas, models

# --- PRODUTOS ---
def get_produtos(db: Session):
    return db.query(models.Produto).all()

def get_produto_by_id(db: Session, produto_id: int):
    return db.query(models.Produto).filter(models.Produto.id == produto_id).first()

def create_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def update_produto(db: Session, produto_id: int, dados: schemas.ProdutoCreate):
    db_produto = get_produto_by_id(db, produto_id)
    if db_produto:
        db_produto.nome = dados.nome
        db_produto.descricao = dados.descricao
        db_produto.categoria = dados.categoria
        db_produto.precoUnidade = dados.precoUnidade
        db_produto.peso = dados.peso
        db_produto.quantidadeEstoque = dados.quantidadeEstoque
        db_produto.estoqueMinimo = dados.estoqueMinimo
        db.commit()
        db.refresh(db_produto)
    return db_produto

def delete_produto(db: Session, produto_id: int):
    db_produto = get_produto_by_id(db, produto_id)
    if db_produto:
        db.delete(db_produto)
        db.commit()
    return db_produto

# --- MOVIMENTAÇÕES (UNIFICADO) ---
def create_movimentacao(db: Session, mov: schemas.MovimentacaoCreate):
    produto = get_produto_by_id(db, mov.produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if mov.tipo == "saida":
        if produto.quantidadeEstoque < mov.quantidade:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente. Disponível: {produto.quantidadeEstoque}"
            )
        produto.quantidadeEstoque -= mov.quantidade
    elif mov.tipo == "entrada":
        produto.quantidadeEstoque += mov.quantidade
    else:
        raise HTTPException(status_code=400, detail="Tipo de movimentação inválido")

    db_mov = models.MovimentacaoProduto(**mov.model_dump())
    db.add(db_mov)
    db.commit()
    db.refresh(db_mov)
    return db_mov

def get_movimentacoes(db: Session):
    return db.query(models.MovimentacaoProduto).order_by(models.MovimentacaoProduto.id.desc()).all()