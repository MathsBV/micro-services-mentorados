from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional

from ..config.database import get_db
from ..models.user import User
from ..auth.jwt_handler import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register")
async def register(
    nome: str,
    email: str,
    senha: str,
    telefone: Optional[str] = None,
    area_interesse: Optional[str] = None,
    nivel_experiencia: Optional[str] = None,
    objetivos: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Verificar se o email já existe
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    
    # Criar novo usuário
    hashed_password = User.get_password_hash(senha)
    db_user = User(
        nome=nome,
        email=email,
        telefone=telefone,
        senha_hash=hashed_password,
        area_interesse=area_interesse,
        nivel_experiencia=nivel_experiencia,
        objetivos=objetivos
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Criar token de acesso
    access_token = create_access_token(
        data={"sub": db_user.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "nome": db_user.nome,
            "email": db_user.email
        }
    }

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Buscar usuário
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Criar token de acesso
    access_token = create_access_token(
        data={"sub": user.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "nome": user.nome,
            "email": user.email
        }
    }

@router.get("/me")
async def read_users_me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = verify_token(token)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return {
        "id": user.id,
        "nome": user.nome,
        "email": user.email,
        "area_interesse": user.area_interesse,
        "nivel_experiencia": user.nivel_experiencia
    } 