from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Mentoria(db.Model):
    __tablename__ = "mentorias"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mentorado_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data_agendada = db.Column(db.DateTime, nullable=False)
    duracao = db.Column(db.Integer)  # Duração em minutos
    status = db.Column(db.String(20), default='agendada')  # agendada, concluída, cancelada
    plataforma = db.Column(db.String(50))
    link_reuniao = db.Column(db.String(200))
    notas = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'mentor_id': self.mentor_id,
            'mentorado_id': self.mentorado_id,
            'data_agendada': self.data_agendada.isoformat(),
            'duracao': self.duracao,
            'status': self.status,
            'plataforma': self.plataforma,
            'link_reuniao': self.link_reuniao,
            'notas': self.notas,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 