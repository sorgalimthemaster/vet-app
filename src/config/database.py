from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configurar las URLs de conexión a las bases de datos
SQLALCHEMY_DATABASE_URL_VETERINARIA = os.getenv("DATABASE_URL")

# Crear motores de base de datos
engine_veterinaria = create_engine(SQLALCHEMY_DATABASE_URL_VETERINARIA)

# Crear sesiones de base de datos
SessionLocalVeterinaria = sessionmaker(autocommit=False, autoflush=False, bind=engine_veterinaria)

# Crear bases de datos base
BaseVeterinaria = declarative_base()

def get_db_veterinaria():
    db = None
    try:
        db = SessionLocalVeterinaria()
        yield db
    finally:
        if db:
            db.close()
