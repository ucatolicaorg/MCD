from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.avances import Avance
from app.models.premios import Premio
from app.models.problemas import Problema

router = APIRouter()

@router.post("/{estudiante_id}/{problema_id}", summary="Resolver problema y actualizar avance")
def resolver_problemas(estudiante_id: int, problema_id: int, db: Session = Depends(get_db)):
    # Buscar el problema
    problema = db.query(Problema).filter(Problema.id == problema_id).first()
    if not problema:
        raise HTTPException(status_code=404, detail="Problema no encontrado")

    # Buscar el avance del estudiante en la competencia de este problema
    avance = db.query(Avance).filter(
        Avance.estudiante_id == estudiante_id,
        Avance.competencia == problema.competencia.nombre
    ).first()

    # Si no existe avance, crear uno nuevo
    if not avance:
        avance = Avance(
            estudiante_id=estudiante_id,
            competencia=problema.competencia.nombre,
            porcentaje_avance=0
        )
        db.add(avance)
        db.commit()
        db.refresh(avance)

    # Aumentar el porcentaje de avance
    avance.porcentaje_avance += problema.puntos_problema

    # Controlar que no pase de 100% avance
    if avance.porcentaje_avance > 100:
        avance.porcentaje_avance = 100

    db.commit()
    db.refresh(avance)

    # Otorgar premio si el porcentaje es 100%
    if avance.porcentaje_avance == 100:
        nuevo_premio = Premio(
            nombre="Medalla de Finalización",
            descripcion=f"Completaste la competencia: {problema.competencia.nombre}",
            estudiante_id=estudiante_id,
            fecha_otorgado=date.today()
        )
        db.add(nuevo_premio)
        db.commit()

    return {
        "message": "Problema resuelto exitosamente",
        "avance_actual": avance.porcentaje_avance
    }
