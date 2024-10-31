from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class TokenSchema(BaseModel):
    token: str
    access_token_expires: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class PropietarioBase(BaseModel):
    nombre: str
    apellidopat: str
    apellidomat: str
    telefono: str

class PropietarioCreate(PropietarioBase):
    pass

class Propietario(PropietarioBase):
    id_propietario: int

    class Config:
        from_attributes = True

class MascotaBase(BaseModel):
    nombre_mascota: str
    raza: str
    año_nacimiento: int

class MascotaCreate(MascotaBase):
    id_propietario: int

class Mascota(MascotaBase):
    id_mascota: int
    id_propietario: int

    class Config:
        from_attributes = True

class ConsultaBase(BaseModel):
    id_mascota: int
    consulta: str
    fecha: Optional[date] = None  # Hacer que fecha sea opcional

class ConsultaCreate(ConsultaBase):
    pass

class Consulta(ConsultaBase):
    id: int

    class Config:
        from_attributes = True
