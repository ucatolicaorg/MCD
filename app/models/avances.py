from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Avance(Base):
    __tablename__ = "avances"

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, index=True)
    competencia = Column(String)
    porcentaje_avance = Column(Float)

