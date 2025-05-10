from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.database import engine, Base
from .routes import auth

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Mentoria")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "API de Mentoria"} 