import os

# Configurações do banco de dados
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configurações do CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Configurações do Gunicorn para produção
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5
errorlog = "logs/error.log"
accesslog = "logs/access.log"
loglevel = "info"

# Configurações de segurança
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configurações de performance
max_requests = 1000
max_requests_jitter = 50
worker_connections = 1000 