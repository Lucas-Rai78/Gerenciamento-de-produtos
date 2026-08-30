
### criar e ativar o ambiente virtual (venv)
python3 -m venv venv
#### windows
.\venv\Scripts\activate
#### linux
source venv/bin/activate
___
### instalar as dependencias
pip install -r requirements.txt
___
### executar o backend
uvicorn app.main:app --reload
___
### link da interface interativa
http://127.0.0.1:8000/docs #swagger ui, interface interativa
___
### utilizar a extensão Live Server para rodar o frontend
___

Adicionar: barra de pesquisa, preço da saída, formulários em pop-up