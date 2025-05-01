from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# ------------------------------
# Modelos para Usuarios
# ------------------------------
class UsuarioBase(BaseModel):
    nombre: str
    correo: str
    es_profesor: bool = False

class UsuarioCreate(BaseModel):
    nombre: str
    correo: str
    password: str
    es_profesor: bool = False
    
class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True  

# ------------------------------
# Modelos para Competencias
# ------------------------------
class CompetenciaBase(BaseModel):
    nombre: str
    descripcion: str

class CompetenciaCreate(CompetenciaBase):
    pass

class CompetenciaResponse(CompetenciaBase):
    id: int

    class Config:
        from_attributes = True  

# ------------------------------
# Modelos para Avances
# ------------------------------
class AvanceBase(BaseModel):
    estudiante_id: int
    competencia: str  
    porcentaje_avance: float  

class AvanceCreate(AvanceBase):
    pass

class AvanceUpdate(BaseModel):
    porcentaje_avance: float  

class AvanceResponse(AvanceBase):
    id: int

    class Config:
        from_attributes = True  

# ------------------------------
# Modelos para Problemas
# ------------------------------
class ProblemaBase(BaseModel):
    id: int
    titulo: str
    descripcion: str
    puntos_problema: int
    competencia_id: int
    
class ProblemaCreate(ProblemaBase):
    pass

class ProblemaResponse(ProblemaBase):
    id: int

    class Config:
        from_attributes = True  

# ------------------------------
# Modelos para Premios
# ------------------------------
class PremioBase(BaseModel):
    estudiante_id: int
    descripcion: str
    fecha_otorgado: date  

class PremioCreate(PremioBase):
    nombre: str  

class PremioResponse(PremioBase):
    id: int  

    class Config:
        from_attributes = True  




