from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    senha_hash = db.Column(db.String(128))
    area_interesse = db.Column(db.String(100))
    nivel_experiencia = db.Column(db.String(50))
    objetivos = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    mentorias_mentor = db.relationship('Mentoria', foreign_keys='Mentoria.mentor_id', backref='mentor', lazy=True)
    mentorias_mentorado = db.relationship('Mentoria', foreign_keys='Mentoria.mentorado_id', backref='mentorado', lazy=True)

    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.senha_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'area_interesse': self.area_interesse,
            'nivel_experiencia': self.nivel_experiencia,
            'objetivos': self.objetivos,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 