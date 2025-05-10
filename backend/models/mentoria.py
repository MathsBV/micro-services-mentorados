from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..config.database import Base

class Mentoria(Base):
    __tablename__ = "mentorias"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String)
    mentor_id = Column(Integer, ForeignKey("users.id"))
    mentorado_id = Column(Integer, ForeignKey("users.id"))
    data_agendada = Column(DateTime(timezone=True))
    duracao = Column(Integer)  # duração em minutos
    status = Column(String)  # agendada, concluída, cancelada
    plataforma = Column(String)  # zoom, google meet, etc
    link_reuniao = Column(String)
    notas = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    mentor = relationship("User", foreign_keys=[mentor_id])
    mentorado = relationship("User", foreign_keys=[mentorado_id]) 