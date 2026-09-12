from sqlalchemy.orm import Session
from app.modules.movimentacoes.models import models


def create_movimentacao(db: Session, db_mov: models.MovimentacaoProduto):
    db.add(db_mov)
    db.commit()
    db.refresh(db_mov)
    return db_mov


def get_movimentacoes(db: Session):
    return (
        db.query(models.MovimentacaoProduto)
        .order_by(models.MovimentacaoProduto.id.desc())
        .all()
    )