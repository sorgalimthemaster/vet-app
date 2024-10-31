from datetime import datetime, timedelta
import secrets
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from controllers.crud import get_user_by_username
from config.database import get_db_veterinaria
from models.models import Token, User

SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


def create_and_store_token(db: Session, expires_in_minutes: int = 30):
    token_value = secrets.token_hex(16)
    access_token_expires = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    token = Token(token=token_value, access_token_expires=access_token_expires)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token

def validate_token(token: HTTPAuthorizationCredentials, db: Session = Depends(get_db_veterinaria)):
    # Busca el token en la base de datos
    db_token = db.query(Token).filter(Token.token == token.credentials).first()

    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Verifica si el token ha expirado
    if db_token.access_token_expires < datetime.utcnow():
        # Elimina el token expirado
        db.delete(db_token)
        db.commit()

        # Genera y almacena un nuevo token
        db_token = create_and_store_token(db)

    # Obtén el usuario asociado al token
    user = db.query(Token).filter(Token.token == db_token).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
