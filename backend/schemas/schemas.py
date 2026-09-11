from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal

# --- SCHEMAS DE PRODUTO ---

class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, description="Nome do produto")
    descricao: str = Field(..., max_length=255, description="Descrição detalhada")
    categoria: str = Field(..., min_length=2, max_length=50)
    precoUnidade: float = Field(..., gt=0, description="Preço unitário deve ser maior que zero")
    peso: str = Field(..., min_length=1, max_length=20)
    quantidadeEstoque: int = Field(..., ge=0, description="Estoque não pode ser negativo")
    estoqueMinimo: int = Field(0, ge=0, description="Estoque mínimo não pode ser negativo")

    @field_validator("categoria")
    @classmethod
    def sanitizar_strings(cls, v: str) -> str:
        return v.strip()


class ProdutoCreate(ProdutoBase):
    @field_validator("nome")
    @classmethod
    def validar_nome_sem_numeros(cls, v: str) -> str:
        nome_limpo = v.strip()
        if any(char.isdigit() for char in nome_limpo):
            raise ValueError("O nome do produto não pode conter números.")
        return nome_limpo

    @field_validator("descricao")
    @classmethod
    def validar_descricao_sem_numeros(cls, v: str) -> str:
        desc_limpa = v.strip()
        if any(char.isdigit() for char in desc_limpa):
            raise ValueError("A descrição do produto não pode conter números.")
        return desc_limpa


class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True

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