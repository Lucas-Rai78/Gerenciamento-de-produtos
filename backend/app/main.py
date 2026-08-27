from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud, models
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gerenciador de produtos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/produtos/", response_model=schemas.ProdutoResponse, status_code=201)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.create_produto(db=db, produto=produto)

@app.get("/produtos/", response_model=List[schemas.ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return crud.get_produtos(db=db)

@app.get("/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = crud.get_produto_by_id(db=db, produto_id=produto_id)
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@app.put("/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def atualizar_produto(produto_id: int, dados: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = crud.update_produto(db=db, produto_id=produto_id, dados=dados)
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = crud.delete_produto(db=db, produto_id=produto_id)
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"mensagem": "Produto removido com sucesso"}

@app.post("/entradas/", response_model=schemas.EntradaResponse, status_code=201)
def registrar_entrada(entrada: schemas.EntradaCreate, db: Session = Depends(get_db)):
    return crud.create_entrada(db=db, entrada=entrada)

@app.get("/entradas/", response_model=List[schemas.EntradaResponse])
def listar_entradas(db: Session = Depends(get_db)):
    return crud.get_entradas(db=db)

@app.post("/saidas/", response_model=schemas.SaidaResponse, status_code=201)
def registrar_saida(saida: schemas.SaidaCreate, db: Session = Depends(get_db)):
    return crud.create_saida(db=db, entrada=saida)

@app.get("/saidas/", response_model=List[schemas.SaidaResponse])
def listar_saidas(db: Session = Depends(get_db)):
    return crud.get_saidas(db=db)