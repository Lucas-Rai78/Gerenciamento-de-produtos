from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    categoria = Column(String)
    precoUnidade = Column(Float)
    peso = Column(String)
    quantidadeEstoque = Column(Integer, default=0)
    estoqueMinimo = Column(Integer, default=0)

    entradas = relationship("EntradaProduto", back_populates="produto")
    saidas = relationship("SaidaProduto", back_populates="produto")
    
class EntradaProduto(Base):
    __tablename__ = "entradas_produtos"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    classificacao = Column(String)  # 'compra' ou 'producao'
    unidadeMedida = Column(String)
    quantidade = Column(Integer)
    precoUnitario = Column(Float)
    dataEntrada = Column(String)
    validade = Column(String, nullable=True)

    produto = relationship("Produto", back_populates="entradas")

class SaidaProduto(Base):
    __tablename__ = "saidas_produtos"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    motivo = Column(String)  # 'venda', 'descarte' ou 'producao'
    unidadeMedida = Column(String)
    quantidade = Column(Integer)
    dataSaida = Column(String)

    produto = relationship("Produto", back_populates="saidas")