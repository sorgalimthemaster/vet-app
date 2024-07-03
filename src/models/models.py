from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from config.database import BaseVeterinaria
from sqlalchemy.orm import relationship

class User(BaseVeterinaria):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

class Propietario(BaseVeterinaria):
    __tablename__ = "propietario"
    
    id_propietario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellidopat = Column(String, index=True)
    apellidomat = Column(String, index=True)
    telefono = Column(String, index=True)

    mascotas = relationship("Mascota", back_populates="propietario")

class Mascota(BaseVeterinaria):
    __tablename__ = "mascota"
    
    id_mascota = Column(Integer, primary_key=True, index=True)
    id_propietario = Column(Integer, ForeignKey("propietario.id_propietario"))
    nombre_mascota = Column(String, index=True)
    raza = Column(String, index=True)
    año_nacimiento = Column(Integer)
    
    propietario = relationship("Propietario", back_populates="mascotas")
    consultas = relationship("Consulta", back_populates="mascota")

class Consulta(BaseVeterinaria):
    __tablename__ = "consulta"
    
    id = Column(Integer, primary_key=True, index=True)
    id_mascota = Column(Integer, ForeignKey("mascota.id_mascota"))
    consulta = Column(String)
    fecha = Column(Date)
    
    mascota = relationship("Mascota", back_populates="consultas")
