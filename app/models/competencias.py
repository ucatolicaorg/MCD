from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Competencia(Base):
    __tablename__ = "competencias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String, nullable=True)
    profesor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)  # Relación con el usuario que la crea
