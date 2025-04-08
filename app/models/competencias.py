from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Competencia(Base):
    __tablename__ = "competencias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String, nullable=True)

    profesor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    # Relaciones explícitas
    profesor = relationship(
        "Usuario",
        back_populates="competencias_como_profesor",
        foreign_keys=[profesor_id]
    )

    usuario = relationship(
        "Usuario",
        back_populates="competencias_como_usuario",
        foreign_keys=[usuario_id]
    )

    problemas = relationship("Problema", back_populates="competencia")
