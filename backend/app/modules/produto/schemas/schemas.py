from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal

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