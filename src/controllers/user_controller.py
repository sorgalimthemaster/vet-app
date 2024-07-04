from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from schemas import schemas
from config import auth, database
from services import user_service

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db_veterinaria)):
    return user_service.login_for_access_token(form_data, db)

@router.post("/create_users/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(database.get_db_veterinaria)):
    return user_service.create_user_endpoint(user, db)

@router.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return user_service.read_users_me(current_user)

@router.post("/propietarios/", response_model=schemas.Propietario)
def create_propietario(propietario: schemas.PropietarioCreate, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    return user_service.create_propietario(propietario, db)

@router.post("/mascotas/", response_model=schemas.Mascota)
def create_mascota(mascota: schemas.MascotaCreate, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    return user_service.create_mascota(mascota, db)

@router.put("/propietarios/{id_propietario}", response_model=schemas.Propietario)
def update_propietario(id_propietario: int, propietario: schemas.PropietarioCreate, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    return user_service.update_propietario(id_propietario, propietario, db)

@router.put("/mascotas/{id_mascota}", response_model=schemas.Mascota)
def update_mascota(id_mascota: int, mascota: schemas.MascotaCreate, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    return user_service.update_mascota(id_mascota, mascota, db)

@router.get("/propietarios/", response_model=List[schemas.Propietario])
def read_propietarios(nombre: Optional[str] = None, apellidopat: Optional[str] = None, apellidomat: Optional[str] = None, telefono: Optional[str] = None, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    return user_service.read_propietarios(nombre, apellidopat, apellidomat, telefono, db)

@router.get("/propietarios/{id_propietario}/mascotas", response_model=List[schemas.Mascota])
def read_mascotas_by_propietario(id_propietario: int, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    return user_service.read_mascotas_by_propietario(id_propietario, db)

@router.get("/consultas/{id_mascota}", response_model=List[schemas.Consulta])
def read_consultas_by_mascota(id_mascota: int, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    return user_service.read_consultas_by_mascota(id_mascota, db)

@router.post("/consultas/", response_model=schemas.Consulta)
def create_consulta(consulta: schemas.ConsultaCreate, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db_veterinaria)):
    return user_service.create_consulta(consulta, db)

@router.put("/consultas/{id}", response_model=schemas.Consulta)
def update_consulta(id: int, consulta: schemas.ConsultaCreate, db: Session = Depends(database.get_db_veterinaria), current_user: schemas.User = Depends(auth.get_current_user)):
    return user_service.update_consulta(id, consulta, db)
