from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configurar las URLs de conexión a las bases de datos
SQLALCHEMY_DATABASE_URL_LOGIN = "postgresql://postgres:root@localhost:5432/login"
SQLALCHEMY_DATABASE_URL_VETERINARIA = "postgresql://postgres:root@localhost:5432/bdveterinaria"

# Crear motores de base de datos
engine_login = create_engine(SQLALCHEMY_DATABASE_URL_LOGIN)
engine_veterinaria = create_engine(SQLALCHEMY_DATABASE_URL_VETERINARIA)

# Crear sesiones de base de datos
SessionLocalLogin = sessionmaker(autocommit=False, autoflush=False, bind=engine_login)
SessionLocalVeterinaria = sessionmaker(autocommit=False, autoflush=False, bind=engine_veterinaria)

# Crear bases de datos base
BaseLogin = declarative_base()
BaseVeterinaria = declarative_base()

def get_db_login():
    db = None
    try:
        db = SessionLocalLogin()
        yield db
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to connect to the login database: {e}")
    finally:
        if db:
            db.close()

def get_db_veterinaria():
    db = None
    try:
        db = SessionLocalVeterinaria()
        yield db
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to connect to the veterinaria database: {e}")
    finally:
        if db:
            db.close()
