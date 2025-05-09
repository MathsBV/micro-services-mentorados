from models import SugestaoSaida
from typing import List
from db import get_connection

def gerar_sugestoes_por_interesse(mentorado_id: str) -> List[SugestaoSaida]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""SELECT 
            T2.NAME,
            T2.MAIL,
            T2.AREAS_OF_ACTIVITY,
            T2.CURRENT_COMPANY
            FROM Users T1
            LEFT JOIN Users T2
                ON LOWER(T1.AREAS_OF_ACTIVITY) = LOWER(T2.AREAS_OF_ACTIVITY) 
            WHERE TRUE 
            AND T1.ID = %s
            AND T2.ROLE = 'Mentor'""", (mentorado_id,))
    sugestoes = cursor.fetchall()

    cursor.close()
    conn.close()

    return [SugestaoSaida(
        name=sugestao['NAME'],
        mail=sugestao['MAIL'],
        areas_of_activity=sugestao['AREAS_OF_ACTIVITY'],
        company_name=sugestao['CURRENT_COMPANY']
    ) for sugestao in sugestoes]
