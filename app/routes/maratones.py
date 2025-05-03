from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.maratones import Maraton
from app.models.problema_maraton import ProblemaMaraton  # Importación clave aquí
from app.models.schemas import MaratonCreate, MaratonResponse
from app.database import get_db

router = APIRouter(prefix="/maratones", tags=["Maratones"])

# Listar maratones
@router.get("/", response_model=list[MaratonResponse])
def listar_maratones(db: Session = Depends(get_db)):
    return db.query(Maraton).all()

# Crear maratón con múltiples problemas
@router.post("/", response_model=MaratonResponse)
def crear_maraton(maraton: MaratonCreate, db: Session = Depends(get_db)):
    # Validación de fechas
    if maraton.fecha_fin <= maraton.fecha_inicio:
        raise HTTPException(
            status_code=400,
            detail="La fecha de fin debe ser posterior a la fecha de inicio"
        )

    # Crear el maratón
    db_maraton = Maraton(
        nombre=maraton.nombre,
        descripcion=maraton.descripcion,
        tiempo_limite=maraton.tiempo_limite,
        fecha_inicio=maraton.fecha_inicio,
        fecha_fin=maraton.fecha_fin
    )
    
    db.add(db_maraton)
    db.commit()
    db.refresh(db_maraton)

    # Crear problemas asociados
    for problema in maraton.problemas:
        db_problema = ProblemaMaraton(
            descripcion=problema.descripcion,
            puntos_problema=problema.puntos_problema,
            maraton_id=db_maraton.id
        )
        db.add(db_problema)
    
    db.commit()
    db.refresh(db_maraton)
    
    return db_maraton


# ... (imports anteriores se mantienen igual)

@router.put("/{id}", response_model=MaratonResponse)
def actualizar_maraton(id: int, maraton: MaratonCreate, db: Session = Depends(get_db)):
    # Obtener el maratón existente
    maraton_db = db.query(Maraton).filter(Maraton.id == id).first()
    if not maraton_db:
        raise HTTPException(status_code=404, detail="Maratón no encontrado")

    # Actualizar campos básicos
    maraton_db.nombre = maraton.nombre
    maraton_db.descripcion = maraton.descripcion
    maraton_db.tiempo_limite = maraton.tiempo_limite
    maraton_db.fecha_inicio = maraton.fecha_inicio
    maraton_db.fecha_fin = maraton.fecha_fin

    # Eliminar problemas existentes
    db.query(ProblemaMaraton).filter(ProblemaMaraton.maraton_id == id).delete()

    # Añadir nuevos problemas
    for problema in maraton.problemas:
        db_problema = ProblemaMaraton(
            descripcion=problema.descripcion,
            puntos_problema=problema.puntos_problema,
            maraton_id=id
        )
        db.add(db_problema)

    db.commit()
    db.refresh(maraton_db)
    return maraton_db

@router.delete("/{id}")
def eliminar_maraton(id: int, db: Session = Depends(get_db)):
    # No necesitas eliminar manualmente los problemas si tienes cascade="all, delete-orphan"
    maraton_db = db.query(Maraton).filter(Maraton.id == id).first()
    if not maraton_db:
        raise HTTPException(status_code=404, detail="Maratón no encontrado")
    
    db.delete(maraton_db)
    db.commit()
    return {"message": "Maratón eliminado con éxito"}