from pydantic import BaseModel

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
