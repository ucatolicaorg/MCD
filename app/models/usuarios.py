from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    correo = Column(String, unique=True)
    password = Column(String)
    es_profesor = Column(Boolean, default=False)

    # Relaciones simplificadas sin problemas de imports cruzados
    competencias_como_profesor = relationship(
        "Competencia",
        back_populates="profesor",
        foreign_keys="Competencia.profesor_id"
    )

    competencias_como_usuario = relationship(
        "Competencia",
        back_populates="usuario",
        foreign_keys="Competencia.usuario_id"
    )

    premios = relationship("Premio", back_populates="estudiante")
