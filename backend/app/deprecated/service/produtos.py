from typing import Optional

from backend.app.deprecated.database import get_db
from fastapi import Depends, HTTPException
from pytest import Session

from backend.app.deprecated.crud import get_produtos
from backend.app.deprecated.schemas import ProdutoResponse


def get_produto(db: Session = Depends(get_db)) -> Optional[ProdutoResponse]:
    produtos = get_produtos(db)
    if not produtos:
        HTTPException(
            status_code=404, detail="Nenhum produto encontrado"
        )
    return produtos