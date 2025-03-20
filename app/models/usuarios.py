from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    correo = Column(String, unique=True)
    es_profesor = Column(Boolean, default=False)
    
    # 🔥 Agregar relación con Premio
    premios = relationship("Premio", back_populates="estudiante")




    
  
