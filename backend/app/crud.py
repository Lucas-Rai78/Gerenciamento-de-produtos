from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import schemas, models

# PRODUTOS
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

# ENTRADAS (Soma ao estoque existente)
def create_entrada(db: Session, entrada: schemas.EntradaCreate):
    produto = get_produto_by_id(db, entrada.produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db_entrada = models.EntradaProduto(**entrada.model_dump())
    db.add(db_entrada)
    
    # Incrementa a quantidade no produto base
    produto.quantidadeEstoque += entrada.quantidade
    
    db.commit()
    db.refresh(db_entrada)
    return db_entrada

def get_entradas(db: Session):
    return db.query(models.EntradaProduto).all()

# SAÍDAS (Subtrai do estoque existente)
def create_saida(db: Session, saida: schemas.SaidaCreate):
    produto = get_produto_by_id(db, saida.produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    if produto.quantidadeEstoque < saida.quantidade:
        raise HTTPException(
            status_code=400, 
            detail=f"Estoque insuficiente. Disponível: {produto.quantidadeEstoque}"
        )
    
    db_saida = models.SaidaProduto(**saida.model_dump())
    db.add(db_saida)
    
    # Decrementa a quantidade no produto base
    produto.quantidadeEstoque -= saida.quantidade
    
    db.commit()
    db.refresh(db_saida)
    return db_saida

def get_saidas(db: Session):
    return db.query(models.SaidaProduto).all()