from pydantic import BaseModel
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    categoria: str
    precoUnidade: float
    peso: str
    quantidadeEstoque: int
    estoqueMinimo: int

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True


class MovimentacaoBase(BaseModel):
    produto_id: int
    tipo: str  # 'entrada' ou 'saida'
    categoriaMovimentacao: str
    unidadeMedida: str
    quantidade: int
    precoUnitario: Optional[float] = 0.0
    data: str
    validade: Optional[str] = None

class MovimentacaoCreate(MovimentacaoBase):
    pass

class MovimentacaoResponse(MovimentacaoBase):
    id: int

    class Config:
        from_attributes = True