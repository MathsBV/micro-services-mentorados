from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

# Configuração do Flask
app = Flask(__name__)
CORS(app)

# Configurações
app.config['SQLALCHEMY_DATABASE_URL'] = os.getenv('DATABASE_URL', 'sqlite:///./mentorados.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua_chave_secreta_aqui')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

# Inicialização das extensões
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Importação dos modelos
from models.user import User
from models.mentoria import Mentoria

# Rotas de autenticação
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Verificar se o email já existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já cadastrado'}), 400
    
    # Criar novo usuário
    user = User(
        nome=data['nome'],
        email=data['email'],
        telefone=data.get('telefone'),
        area_interesse=data.get('area_interesse'),
        nivel_experiencia=data.get('nivel_experiencia'),
        objetivos=data.get('objetivos')
    )
    user.set_password(data['senha'])
    
    db.session.add(user)
    db.session.commit()
    
    # Criar token de acesso
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'token_type': 'bearer',
        'user': {
            'id': user.id,
            'nome': user.nome,
            'email': user.email
        }
    }), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.verify_password(data['senha']):
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'token_type': 'bearer',
        'user': {
            'id': user.id,
            'nome': user.nome,
            'email': user.email
        }
    })

@app.route('/auth/me', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'id': user.id,
        'nome': user.nome,
        'email': user.email,
        'telefone': user.telefone,
        'area_interesse': user.area_interesse,
        'nivel_experiencia': user.nivel_experiencia,
        'objetivos': user.objetivos
    })

# Rotas de mentoria
@app.route('/mentorias', methods=['GET'])
@jwt_required()
def get_mentorias():
    user_id = get_jwt_identity()
    mentorias = Mentoria.query.filter_by(mentorado_id=user_id).all()
    
    return jsonify([{
        'id': m.id,
        'titulo': m.titulo,
        'descricao': m.descricao,
        'data_agendada': m.data_agendada.isoformat(),
        'status': m.status,
        'plataforma': m.plataforma
    } for m in mentorias])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True) 