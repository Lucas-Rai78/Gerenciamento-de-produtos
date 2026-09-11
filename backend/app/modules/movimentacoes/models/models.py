from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class MovimentacaoProduto(Base):
    __tablename__ = "movimentacoes_produtos"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    tipo = Column(String, nullable=False)  # 'entrada' ou 'saida'
    categoriaMovimentacao = Column(String, nullable=False)  # 'compra', 'producao', 'venda', 'descarte'
    unidadeMedida = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    precoUnitario = Column(Float, default=0.0)
    data = Column(String, nullable=False)
    validade = Column(String, nullable=True)

    produto = relationship("Produto", back_populates="movimentacoes")