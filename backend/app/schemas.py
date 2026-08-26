from pydantic import BaseModel

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