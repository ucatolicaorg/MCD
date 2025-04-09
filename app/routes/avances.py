from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.avances import Avance
from app.models.schemas import AvanceCreate, AvanceUpdate  # Agregamos el esquema para actualización

router = APIRouter(prefix="/avances", tags=["Avances"])

@router.post("", summary="Registrar Avance")
def registrar_avance(avance: AvanceCreate, db: Session = Depends(get_db)):
    db_avance = Avance(
        estudiante_id=avance.estudiante_id,
        competencia=avance.competencia,
        porcentaje_avance=avance.porcentaje_avance
    )
    db.add(db_avance)
    db.commit()
    db.refresh(db_avance)
    return db_avance

#@router.get("/{estudiante_id}", summary="Obtener Avance")#
@router.get("/{estudiante_id}", summary="Prueba de Cambio 1")
def obtener_avance(estudiante_id: int, db: Session = Depends(get_db)):
    db_avance = db.query(Avance).filter(Avance.estudiante_id == estudiante_id).all()
    if not db_avance:
        raise HTTPException(status_code=404, detail="No se encontraron avances para este estudiante.")
    return db_avance

@router.put("/{id}", summary="Actualizar Avance")
def actualizar_avance(id: int, avance_update: AvanceUpdate, db: Session = Depends(get_db)):
    db_avance = db.query(Avance).filter(Avance.id == id).first()
    if not db_avance:
        raise HTTPException(status_code=404, detail="Avance no encontrado.")
    
    db_avance.porcentaje_avance = avance_update.porcentaje_avance  # Solo actualizamos el porcentaje de avance
    db.commit()
    db.refresh(db_avance)
    return db_avance

@router.delete("/{id}", summary="Eliminar Avance")
def eliminar_avance(id: int, db: Session = Depends(get_db)):
    db_avance = db.query(Avance).filter(Avance.id == id).first()
    if not db_avance:
        raise HTTPException(status_code=404, detail="Avance no encontrado.")
    
    db.delete(db_avance)
    db.commit()
    return {"message": "Avance eliminado exitosamente"}







