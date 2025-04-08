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
        from_attributes = True  # ✅ Compatible con Pydantic V2

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
        from_attributes = True  # ✅ Compatible con Pydantic V2

# ------------------------------
# Modelos para Avances
# ------------------------------
class AvanceBase(BaseModel):
    estudiante_id: int
    competencia: str  # Si es un nombre de competencia, puedes mantenerlo como str
    porcentaje_avance: float  # Debe ser un porcentaje, se usa float

class AvanceCreate(AvanceBase):
    pass

class AvanceUpdate(BaseModel):
    porcentaje_avance: float  # Solo permite actualizar el porcentaje de avance

class AvanceResponse(AvanceBase):
    id: int

    class Config:
        from_attributes = True  # ✅ Compatible con Pydantic V2

# ------------------------------
# Modelos para Problemas
# ------------------------------
class ProblemaBase(BaseModel):
    competencia_id: int
    descripcion: str
    fecha_creacion: datetime  # Usar datetime para la fecha

class ProblemaCreate(ProblemaBase):
    pass

class ProblemaResponse(ProblemaBase):
    id: int

    class Config:
        from_attributes = True  # ✅ Compatible con Pydantic V2

# ------------------------------
# Modelos para Premios
# ------------------------------
class PremioBase(BaseModel):
    estudiante_id: int
    descripcion: str
    fecha_otorgado: date  # Usamos date para la fecha de otorgado

class PremioCreate(PremioBase):
    nombre: str  # Incluir nombre al crear el premio

class PremioResponse(PremioBase):
    id: int  # El ID será asignado por la base de datos

    class Config:
        from_attributes = True  # ✅ Compatible con Pydantic V2




