from fastapi import FastAPI
from models import SugestaoSaida
from gerenciamento import gerar_sugestoes_por_interesse
from typing import List

app = FastAPI()

@app.get("/mentoring-managment/{mentorado_id}", response_model=List[SugestaoSaida])
def sugerir_mentores(mentorado_id: int):
    return gerar_sugestoes_por_interesse(mentorado_id)
