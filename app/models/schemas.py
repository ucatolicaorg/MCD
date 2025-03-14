from pydantic import BaseModel

<<<<<<< HEAD
=======
# Definimos los modelos para Usuarios
>>>>>>> gestion-avances
class UsuarioBase(BaseModel):
    nombre: str
    correo: str
    es_profesor: bool = False

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
<<<<<<< HEAD
=======

# Definimos los modelos para Competencias
class CompetenciaBase(BaseModel):
    nombre: str
    descripcion: str

class CompetenciaCreate(CompetenciaBase):
    pass

class CompetenciaResponse(CompetenciaBase):
    id: int

    class Config:
        orm_mode = True
>>>>>>> gestion-avances
