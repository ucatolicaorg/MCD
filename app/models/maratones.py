# models/maratones.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Maraton(Base):
    __tablename__ = "maratones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String, nullable=True)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)

    # Relación con los problemas
    problemas = relationship("Problema", back_populates="maraton")

    def __repr__(self):
        return f"<Maraton {self.nombre}>"

class Problema(Base):
    __tablename__ = "problemas"
    __table_args__ = {'extend_existing': True}  # Aquí agregamos extend_existing

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    puntos_problema = Column(Integer, nullable=False)
    maraton_id = Column(Integer, ForeignKey("maratones.id"), nullable=False)

    # Relación inversa con Maraton
    maraton = relationship("Maraton", back_populates="problemas")

    def __repr__(self):
        return f"<Problema {self.descripcion}>"



