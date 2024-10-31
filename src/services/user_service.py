from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas import schemas
from controllers import crud
from config import auth
from models import models

def login_for_access_token(form_data: schemas.UserCreate, db: Session):
    try:
        user = crud.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        expires_in_minutes = auth.ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60
        access_token = auth.create_and_store_token(db, expires_in_minutes=expires_in_minutes)
        
        return {"access_token": access_token.token, "token_type": "bearer"}
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}"
        )

def create_user_endpoint(user: schemas.UserCreate, db: Session):
    try:
        db_user = crud.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        return crud.create_user(db=db, user=user)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

def read_users_me(current_user: schemas.User):
    try:
        return current_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching current user: {str(e)}"
        )

def create_propietario(propietario: schemas.PropietarioCreate, db: Session):
    try:
        db_propietario = models.Propietario(**propietario.model_dump())
        db.add(db_propietario)
        db.commit()
        db.refresh(db_propietario)
        return db_propietario
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating propietario: {str(e)}"
        )

def create_mascota(mascota: schemas.MascotaCreate, db: Session):
    try:
        db_mascota = models.Mascota(**mascota.model_dump())
        db.add(db_mascota)
        db.commit()
        db.refresh(db_mascota)
        return db_mascota
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating mascota: {str(e)}"
        )

def update_propietario(id_propietario: int, propietario: schemas.PropietarioCreate, db: Session):
    try:
        db_propietario = db.query(models.Propietario).filter(models.Propietario.id_propietario == id_propietario).first()
        if db_propietario is None:
            raise HTTPException(status_code=404, detail="Propietario not found")
        for key, value in propietario.model_dump().items():
            setattr(db_propietario, key, value)
        db.commit()
        db.refresh(db_propietario)
        return db_propietario
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating propietario: {str(e)}"
        )

def update_mascota(id_mascota: int, mascota: schemas.MascotaCreate, db: Session):
    try:
        db_mascota = db.query(models.Mascota).filter(models.Mascota.id_mascota == id_mascota).first()
        if db_mascota is None:
            raise HTTPException(status_code=404, detail="Mascota not found")
        for key, value in mascota.model_dump().items():
            setattr(db_mascota, key, value)
        db.commit()
        db.refresh(db_mascota)
        return db_mascota
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating mascota: {str(e)}"
        )

def read_propietarios(nombre: Optional[str], apellidopat: Optional[str], apellidomat: Optional[str], telefono: Optional[str], db: Session):
    try:
        query = db.query(models.Propietario)
        if nombre:
            query = query.filter(models.Propietario.nombre == nombre)
        if apellidopat:
            query = query.filter(models.Propietario.apellidopat == apellidopat)
        if apellidomat:
            query = query.filter(models.Propietario.apellidomat == apellidomat)
        if telefono:
            query = query.filter(models.Propietario.telefono == telefono)
        propietarios = query.all()
        return propietarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching propietarios: {str(e)}"
        )

def read_mascotas_by_propietario(id_propietario: int, db: Session):
    try:
        mascotas = db.query(models.Mascota).filter(models.Mascota.id_propietario == id_propietario).all()
        return mascotas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching mascotas by propietario: {str(e)}"
        )

def read_consultas_by_mascota(id_mascota: int, db: Session):
    try:
        consultas = db.query(models.Consulta).filter(models.Consulta.id_mascota == id_mascota).all()
        return consultas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching consultas by mascota: {str(e)}"
        )

def create_consulta(consulta: schemas.ConsultaCreate, db: Session):
    try:
        db_consulta = models.Consulta(
            id_mascota=consulta.id_mascota,
            consulta=consulta.consulta,
            fecha=datetime.now()
        )
        db.add(db_consulta)
        db.commit()
        db.refresh(db_consulta)
        return db_consulta
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating consulta: {str(e)}"
        )

def update_consulta(id: int, consulta: schemas.ConsultaCreate, db: Session):
    try:
        db_consulta = db.query(models.Consulta).filter(models.Consulta.id == id).first()
        if db_consulta is None:
            raise HTTPException(status_code=404, detail="Consulta not found")
        for key, value in consulta.model_dump().items():
            setattr(db_consulta, key, value)
        db.commit()
        db.refresh(db_consulta)
        return db_consulta
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating consulta: {str(e)}"
        )
