from models import SugestaoSaida
from typing import List
from db import get_connection

def gerar_sugestoes_por_interesse(mentored_id: int) -> List[SugestaoSaida]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""SELECT T2.ID 
                    ,T3.NAME AS MENTORING_NAME
                    ,T2.NAME AS MENTOR_NAME
                    ,T2.SCHEDULED_DATE
                    ,T2.RATING
                    FROM Users T1
                    LEFT JOIN Mentoring T2
                    	ON T1.ID = T2.MENTORED_ID
                    LEFT JOIN Users T3
                    	ON T2.MENTOR_ID = T3.ID
                    WHERE TRUE
                    AND MENTORED_ID = %s
                    AND TIMESTAMPDIFF(MINUTE,SCHEDULED_DATE,NOW()) > 0""", (mentored_id,))
    feedbacks = cursor.fetchall()

    cursor.close()
    conn.close()

    return [SugestaoSaida(
        id=feedback['ID'],
        mentor_name=feedback['MENTORING_NAME'],
        mentoring_name=feedback['MENTOR_NAME'],
        scheduled_date=feedback['SCHEDULED_DATE'],
        mentoring_rating=feedback['RATING']
    ) for feedback in feedbacks]
