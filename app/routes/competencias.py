from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.competencias import Competencia
from app.models.schemas import CompetenciaCreate, CompetenciaResponse
from app.routes.auth import get_current_user  # ✅ Corrección aquí

router = APIRouter(prefix="/competencias", tags=["Competencias"])

# 📌 Obtener todas las competencias (Disponible para todos)
@router.get("/", response_model=list[CompetenciaResponse])
def listar_competencia(db: Session = Depends(get_db)):
    return db.query(Competencia).all()

# 📌 Crear una nueva competencia (Solo profesores)
@router.post("/", response_model=CompetenciaResponse)
def crear_competencia(competencia: CompetenciaCreate, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    if not usuario.es_profesor:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo los profesores pueden crear competencias.")
    
    # Aquí asignamos el ID del profesor que está autenticado
    nueva_competencia = Competencia(
        nombre=competencia.nombre,
        descripcion=competencia.descripcion,
        profesor_id=usuario.id,  # Asignamos el ID del profesor
        usuario_id=usuario.id  # Puedes asignar el usuario_id si lo necesitas
    )
    
    db.add(nueva_competencia)
    db.commit()
    db.refresh(nueva_competencia)
    return nueva_competencia


# 📌 Editar competencia (Solo profesores)
@router.put("/{id}", response_model=CompetenciaResponse)
def editar_competencia(id: int, competencia: CompetenciaCreate, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    if not usuario.es_profesor:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo los profesores pueden editar competencias.")

    competencia_db = db.query(Competencia).filter(Competencia.id == id).first()
    if not competencia_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competencia no encontrada")

    competencia_db.nombre = competencia.nombre
    competencia_db.descripcion = competencia.descripcion
    db.commit()
    db.refresh(competencia_db)
    return competencia_db

# 📌 Eliminar competencia (Solo profesores)
@router.delete("/{id}")
def eliminar_competencia(id: int, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    if not usuario.es_profesor:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo los profesores pueden eliminar competencias.")

    competencia_db = db.query(Competencia).filter(Competencia.id == id).first()
    if not competencia_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competencia no encontrada")

    db.delete(competencia_db)
    db.commit()
    return {"message": "Competencia eliminada exitosamente"}
