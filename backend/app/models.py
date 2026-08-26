from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    categoria = Column(String)
    precoUnidade = Column(Float)
    peso = Column(String)
    quantidadeEstoque = Column(Integer)
    estoqueMinimo = Column(Integer)