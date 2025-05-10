from pydantic import BaseModel

class SugestaoSaida(BaseModel):
    name: str
    mail: str
    areas_of_activity: str
    company_name: str
