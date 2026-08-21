from sqlalchemy.orm import Session
from app import models, schemas

def get_produtos(db: Session):
    return db.query(models.Produto).all()

def get_produto_by_id(db: Session, produto_id: int):
    return db.query(models.Produto).filter(models.Produto.id == produto_id).first(
        
    )
def create_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto   

def update_produto(db: Session, produto_id: int, dados: schemas.ProdutoCreate):
    db_produto = get_produto_by_id (db, produto_id)
    if db_produto:
        db_produto.nome = dados.nome
        db_produto.descricao = dados.descricao
        db_produto.preco = dados.preco
        db_produto.estoque = dados.estoque
        db_produto.validade = dados.validade
        db_produto.peso = dados.peso
        db.commit()
        db.refresh(db_produto)
    return db_produto

def delete_produto(db: Session, produto_id: int):
    db_produto = get_produto_by_id(db, produto_id)
    if db_produto:
        db.delete(db_produto)
        db.commit()
    return db_produto