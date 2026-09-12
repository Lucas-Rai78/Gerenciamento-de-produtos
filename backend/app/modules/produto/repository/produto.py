from sqlalchemy.orm import Session
from app.modules.produto.models import models


def get_produtos(db: Session):
    return db.query(models.Produto).all()


def get_produto_by_id(db: Session, produto_id: int):
    return db.query(models.Produto).filter(models.Produto.id == produto_id).first()


def create_produto(db: Session, db_produto: models.Produto):
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


def update_produto(db: Session, db_produto: models.Produto, dados: dict):
    for chave, valor in dados.items():
        setattr(db_produto, chave, valor)

    db.commit()
    db.refresh(db_produto)
    return db_produto


def delete_produto(db: Session, db_produto: models.Produto):
    db.delete(db_produto)
    db.commit()
    return db_produto