import os

# Configurações do banco de dados
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mentorados.db")

# Configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configurações do CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# Configurações do Gunicorn
bind = "0.0.0.0:8000"
workers = 4  # Ajuste conforme necessário
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5
errorlog = "logs/error.log"
accesslog = "logs/access.log"
loglevel = "info" 