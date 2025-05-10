from fastapi import FastAPI
from backend.micro_gerenciamento.main import app as gerenciamento_app
from backend.micro_feedback.main import app as feedback_app
from backend.micro_sugestao.main import app as sugestao_app
from backend.micro_notificacao.main import app as notificacao_app

app = FastAPI()

# Monta os microserviços
app.mount("/gerenciamento", gerenciamento_app)
app.mount("/feedback", feedback_app)
app.mount("/sugestao", sugestao_app)
app.mount("/notificacao", notificacao_app) 