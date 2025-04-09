from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Premio(Base):
    __tablename__ = "premios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)
    estudiante_id = Column(Integer, ForeignKey("usuarios.id"))  # 🔥 Clave foránea a Usuario
    fecha_otorgado = Column(Date)

    # 🔥 Relación con Usuario
    estudiante = relationship("Usuario", back_populates="premios")


