from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine
from app.modules.produto.models import models as produto_models
from app.modules.movimentacoes.models import models as movimentacao_models
from app.modules.produto.endpoints.endpoints import router as produto_router
from app.modules.movimentacoes.endpoints.endpoints import router as movimentacao_router

produto_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gerenciador de Estoque - LaPiazza")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(produto_router)
app.include_router(movimentacao_router)