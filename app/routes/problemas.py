from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.problemas import Problema
from app.models.competencias import Competencia  # Asegúrate de importar Competencia
from app.models.schemas import ProblemaCreate, ProblemaResponse
from typing import List

router = APIRouter(prefix="/problemas", tags=["Problemas"])

@router.post("", response_model=ProblemaResponse, summary="Crear Problema")
def crear_problema(problema: ProblemaCreate, db: Session = Depends(get_db)):
    # Verificar que la competencia existe
    competencia = db.query(Competencia).filter(Competencia.id == problema.competencia_id).first()
    if not competencia:
        raise HTTPException(status_code=404, detail="Competencia no encontrada")

    nuevo_problema = Problema(
        titulo=problema.titulo,
        descripcion=problema.descripcion,
        competencia_id=problema.competencia_id,
        puntos_problema=problema.puntos_problema
    )
    db.add(nuevo_problema)
    db.commit()
    db.refresh(nuevo_problema)
    return nuevo_problema

@router.get("/{competencia_id}", response_model=List[ProblemaResponse], summary="Ver Problemas")
def ver_problemas(competencia_id: int, db: Session = Depends(get_db)):
    # Verificar que la competencia existe
    competencia = db.query(Competencia).filter(Competencia.id == competencia_id).first()
    if not competencia:
        raise HTTPException(status_code=404, detail="Competencia no encontrada")

    problemas = db.query(Problema).filter(Problema.competencia_id == competencia_id).all()
    return problemas or []




