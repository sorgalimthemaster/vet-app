from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from schemas import schemas
from controllers import crud
from config import auth, database
from models import models

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db_login)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=auth.ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/create_users/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(database.get_db_login)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

@router.post("/propietarios/", response_model=schemas.Propietario)
def create_propietario(propietario: schemas.PropietarioCreate, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    db_propietario = models.Propietario(**propietario.model_dump())
    db.add(db_propietario)
    db.commit()
    db.refresh(db_propietario)
    return db_propietario

@router.post("/mascotas/", response_model=schemas.Mascota)
def create_mascota(mascota: schemas.MascotaCreate, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    db_mascota = models.Mascota(**mascota.model_dump())
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

@router.put("/propietarios/{id_propietario}", response_model=schemas.Propietario)
def update_propietario(id_propietario: int, propietario: schemas.PropietarioCreate, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    db_propietario = db.query(models.Propietario).filter(models.Propietario.id_propietario == id_propietario).first()
    if db_propietario is None:
        raise HTTPException(status_code=404, detail="Propietario not found")
    for key, value in propietario.model_dump().items():
        setattr(db_propietario, key, value)
    db.commit()
    db.refresh(db_propietario)
    return db_propietario

@router.put("/mascotas/{id_mascota}", response_model=schemas.Mascota)
def update_mascota(id_mascota: int, mascota: schemas.MascotaCreate, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    db_mascota = db.query(models.Mascota).filter(models.Mascota.id_mascota == id_mascota).first()
    if db_mascota is None:
        raise HTTPException(status_code=404, detail="Mascota not found")
    for key, value in mascota.model_dump().items():
        setattr(db_mascota, key, value)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

@router.get("/propietarios/", response_model=List[schemas.Propietario])
def read_propietarios(nombre: Optional[str] = None, apellidopat: Optional[str] = None, apellidomat: Optional[str] = None, telefono: Optional[str] = None, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
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

@router.get("/propietarios/{id_propietario}/mascotas", response_model=List[schemas.Mascota])
def read_mascotas_by_propietario(id_propietario: int, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    mascotas = db.query(models.Mascota).filter(models.Mascota.id_propietario == id_propietario).all()
    return mascotas

@router.get("/consultas/{id_mascota}", response_model=List[schemas.Consulta])
def read_consultas_by_mascota(id_mascota: int, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    consultas = db.query(models.Consulta).filter(models.Consulta.id_mascota == id_mascota).all()
    return consultas

@router.post("/consultas/", response_model=schemas.Consulta)
def create_consulta(consulta: schemas.ConsultaCreate, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db_veterinaria)):
    db_consulta = models.Consulta(
        id_mascota=consulta.id_mascota,
        consulta=consulta.consulta,
        fecha=datetime.now()
    )
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

@router.put("/consultas/{id}", response_model=schemas.Consulta)
def update_consulta(id: int, consulta: schemas.ConsultaCreate, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    db_consulta = db.query(models.Consulta).filter(models.Consulta.id == id).first()
    if db_consulta is None:
        raise HTTPException(status_code=404, detail="Consulta not found")
    for key, value in consulta.model_dump().items():
        setattr(db_consulta, key, value)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta
