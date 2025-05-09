from fastapi import FastAPI
from models import SugestaoSaida
from sugestao import gerar_sugestoes_por_interesse
from typing import List

app = FastAPI()

@app.get("/sugestion/{mentorado_id}", response_model=List[SugestaoSaida])
def sugerir_mentores(mentorado_id: int):
    return gerar_sugestoes_por_interesse(mentorado_id)
