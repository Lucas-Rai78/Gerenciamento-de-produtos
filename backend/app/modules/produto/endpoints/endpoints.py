from fastapi import FastAPI, Depends, status, app
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
  

from app.database.database import get_db
from app.modules.schemas import schemas
from app.modules.service import crud

@app.post("/produtos", response_model=schemas.ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.create_produto(db=db, produto=produto)

@app.get("/produtos", response_model=List[schemas.ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return crud.get_produtos(db=db)

@app.get("/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    return crud.get_produto_by_id(db=db, produto_id=produto_id)

@app.put("/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def atualizar_produto(produto_id: int, dados: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.update_produto(db=db, produto_id=produto_id, dados=dados)

@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    return crud.delete_produto(db=db, produto_id=produto_id)