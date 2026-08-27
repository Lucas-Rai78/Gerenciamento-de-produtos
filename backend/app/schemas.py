from pydantic import BaseModel
from typing import Optional, List

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

class EntradaBase(BaseModel):
    produto_id: int
    classificacao: str
    unidadeMedida: str
    quantidade: int
    precoUnitario: float
    dataEntrada: str
    validade: Optional[str] = None

class EntradaCreate(EntradaBase):
    pass

class EntradaResponse(EntradaBase):
    id: int

    class Config:
        from_attributes = True

class SaidaBase(BaseModel):
    produto_id: int
    motivo: str
    unidadeMedida: str
    quantidade: int
    dataSaida: str

class SaidaCreate(SaidaBase):
    pass

class SaidaResponse(SaidaBase):
    id: int

    class Config:
        from_attributes = True