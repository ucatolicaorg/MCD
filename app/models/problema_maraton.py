from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.maratones import Maraton  # Importación para la relación

class ProblemaMaraton(Base):
    __tablename__ = "problemas_maraton"
    
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    puntos_problema = Column(Integer, nullable=False)
    maraton_id = Column(Integer, ForeignKey("maratones.id"), nullable=False)
    
    maraton = relationship("Maraton", back_populates="problemas")  # Relación inversa