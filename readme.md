python3 -m venv venv #ativa o ambiente virtual
.\venv\Script\activate 

uvicorn app.main:app --reload #inicia o servidor de denvolvimento

http://127.0.0.1:8000/docs #swagger ui, interface interativa