from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.usuarios import Usuario
from app.models.schemas import UsuarioCreate, UsuarioResponse
from app.auth.auth import hash_password, verify_password, create_access_token, oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["Autenticación"])

def get_db():

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Clave secreta y algoritmo para JWT
SECRET_KEY = "tu_clave_secreta"
ALGORITHM = "HS256"

def get_db():
    """Función para obtener la sesión de la base de datos"""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UsuarioResponse)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if usuario_db:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        password=hash_password(usuario.password),
        es_profesor=usuario.es_profesor
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo == form_data.username).first()
    
    if not usuario or not verify_password(form_data.password, usuario.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    access_token = create_access_token(data={"sub": usuario.correo})
    return {"access_token": access_token, "token_type": "bearer"}

<<<<<<< HEAD
@router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"message": "Usuario autenticado", "token": token}
=======
# Función para obtener el usuario actual autenticado
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Decodifica el token JWT y obtiene el usuario actual"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pueden validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if usuario is None:
        raise credentials_exception
    return usuario

@router.get("/me")
def read_users_me(usuario: Usuario = Depends(get_current_user)):
    """Devuelve los datos del usuario autenticado"""
    return {
        "nombre": usuario.nombre,
        "correo": usuario.correo,
        "es_profesor": usuario.es_profesor
    }

>>>>>>> gestion-avances
