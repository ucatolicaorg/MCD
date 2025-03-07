from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    correo = Column(String, unique=True, index=True)
    password = Column(String)  # Guardaremos la contraseña hasheada
    es_profesor = Column(Boolean, default=False)  # True = Profesor, False = Estudiante
