from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal

class MovimentacaoBase(BaseModel):
    produto_id: int = Field(..., gt=0, description="ID do produto deve ser um inteiro válido")
    tipo: Literal["entrada", "saida"]
    categoriaMovimentacao: Literal["compra", "producao", "venda", "descarte"]
    unidadeMedida: str = Field(..., min_length=1, max_length=10)
    quantidade: int = Field(..., gt=0, description="Quantidade deve ser maior que zero")
    precoUnitario: Optional[float] = Field(0.0, ge=0, description="Preço não pode ser negativo")
    data: str = Field(..., min_length=10, max_length=10, description="Formato esperado YYYY-MM-DD")
    validade: Optional[str] = None

    @field_validator("categoriaMovimentacao")
    @classmethod
    def validar_categoria_por_tipo(cls, v: str, info) -> str:
        tipo = info.data.get("tipo")
        if tipo == "entrada" and v not in ["compra", "producao"]:
            raise ValueError("Categorias permitidas para entrada: 'compra' ou 'producao'")
        if tipo == "saida" and v not in ["venda", "descarte", "producao"]:
            raise ValueError("Categorias permitidas para saída: 'venda', 'descarte' ou 'producao'")
        return v

class MovimentacaoCreate(MovimentacaoBase):
    pass

class MovimentacaoResponse(MovimentacaoBase):
    id: int

    class Config:
        from_attributes = True