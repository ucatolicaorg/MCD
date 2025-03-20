from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.problemas import Problema
from app.models.schemas import ProblemaCreate, ProblemaResponse
from typing import List

router = APIRouter(prefix="/problemas", tags=["Problemas"])  # 🔥 Configuración correcta del `prefix`

@router.post("", response_model=ProblemaResponse, summary="Crear Problema")  # ✅ SIN `/` INICIAL
def crear_problema(problema: ProblemaCreate, db: Session = Depends(get_db)):
    nuevo_problema = Problema(
        titulo=problema.titulo,
        descripcion=problema.descripcion,
        competencia_id=problema.competencia_id
    )
    db.add(nuevo_problema)
    db.commit()
    db.refresh(nuevo_problema)
    return nuevo_problema

@router.get("/{competencia_id}", response_model=List[ProblemaResponse], summary="Ver Problemas")  # ✅ Nombre claro
def ver_problemas(competencia_id: int, db: Session = Depends(get_db)):
    problemas = db.query(Problema).filter(Problema.competencia_id == competencia_id).all()
    if not problemas:
        raise HTTPException(status_code=404, detail="No se encontraron problemas")
    return problemas






