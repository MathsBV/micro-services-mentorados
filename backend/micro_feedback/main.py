from fastapi import FastAPI
from .models import SugestaoSaida
from .feedback import gerar_sugestoes_por_interesse
from typing import List

app = FastAPI()

@app.get("/feedback/{mentored_id}", response_model=List[SugestaoSaida])
def sugerir_mentores(mentored_id: int):
    return gerar_sugestoes_por_interesse(mentored_id)
