from models import SugestaoSaida
from typing import List
from db import get_connection

def gerar_sugestoes_por_interesse(mentorado_id: str) -> List[SugestaoSaida]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""SELECT 
            T2.ID,
            T2.NAME AS MENTORING_NAME,
            T3.NAME AS MENTOR_NAME,
            T1.NAME AS MENTORED_NAME,
            T2.SCHEDULED_DATE
            FROM Users T1
            LEFT JOIN Mentoring T2
                ON T1.ID = T2.MENTORED_ID
            LEFT JOIN Users T3
                ON T2.MENTOR_ID = T3.ID
            WHERE TRUE 
            AND T2.CONCLUDED IS FALSE
            AND T1.ID = %s""", (mentorado_id,))
    sugestoes = cursor.fetchall()

    cursor.close()
    conn.close()

    return [SugestaoSaida(
        id=sugestao['ID'],
        name=sugestao['MENTORING_NAME'],
        mentor_name=sugestao['MENTOR_NAME'],
        mentored_name=sugestao['MENTORED_NAME'],
        scheduled_date=sugestao['SCHEDULED_DATE']
    ) for sugestao in sugestoes]