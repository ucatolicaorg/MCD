from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.premios import Premio
from app.models.schemas import PremioCreate, PremioResponse
from typing import List

router = APIRouter(prefix="/premios", tags=["Premios"])  # ✅ PREFIX Y TAGS SON IMPORTANTES

@router.post("/", response_model=PremioResponse)
def asignar_premio(premio: PremioCreate, db: Session = Depends(get_db)):
    nuevo_premio = Premio(
        nombre=premio.nombre,
        descripcion=premio.descripcion,
        estudiante_id=premio.estudiante_id,
        fecha_otorgado=premio.fecha_otorgado
    )
    db.add(nuevo_premio)
    db.commit()
    db.refresh(nuevo_premio)
    return nuevo_premio

@router.get("/{estudiante_id}", response_model=List[PremioResponse])
def ver_premios(estudiante_id: int, db: Session = Depends(get_db)):
    premios = db.query(Premio).filter(Premio.estudiante_id == estudiante_id).all()
    if not premios:
        raise HTTPException(status_code=404, detail="No se encontraron premios")
    return premios




