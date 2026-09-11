from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

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

    movimentacoes = relationship("MovimentacaoProduto", back_populates="produto")