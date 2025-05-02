# routes/maratones.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.maratones import Maraton, Problema
from app.schemas import MaratonCreate, MaratonResponse
from app.database import get_db

router = APIRouter(prefix="/maratones", tags=["Maratones"])

# Listar maratones
@router.get("/", response_model=list[MaratonResponse])
def listar_maratones(db: Session = Depends(get_db)):
    return db.query(Maraton).all()

# Crear maratón con múltiples problemas
@router.post("/", response_model=MaratonResponse)
def crear_maraton(maraton: MaratonCreate, db: Session = Depends(get_db)):
    # Crear el maratón
    nuevo_maraton = Maraton(**maraton.dict(exclude_unset=True))

    # Guardar el maratón en la base de datos para generar su id
    db.add(nuevo_maraton)
    db.commit()
    db.refresh(nuevo_maraton)  # Obtener el id del maratón

    # Agregar los problemas al maratón
    for problema in maraton.problemas:
        nuevo_problema = Problema(
            descripcion=problema.descripcion, 
            puntos_problema=problema.puntos_problema,
            maraton_id=nuevo_maraton.id  # Asociar el problema al maratón
        )
        db.add(nuevo_problema)

    # Guardar los problemas en la base de datos
    db.commit()
    db.refresh(nuevo_maraton)  # Asegúrate de que el maratón y los problemas se hayan guardado
    return nuevo_maraton

# Actualizar maratón
@router.put("/{id}", response_model=MaratonResponse)
def actualizar_maraton(id: int, maraton: MaratonCreate, db: Session = Depends(get_db)):
    maraton_db = db.query(Maraton).filter(Maraton.id == id).first()
    if not maraton_db:
        raise HTTPException(status_code=404, detail="Maratón no encontrado")

    maraton_db.nombre = maraton.nombre
    maraton_db.descripcion = maraton.descripcion
    maraton_db.fecha_inicio = maraton.fecha_inicio
    maraton_db.fecha_fin = maraton.fecha_fin
    db.commit()
    db.refresh(maraton_db)
    return maraton_db

# Eliminar maratón
@router.delete("/{id}")
def eliminar_maraton(id: int, db: Session = Depends(get_db)):
    maraton_db = db.query(Maraton).filter(Maraton.id == id).first()
    if not maraton_db:
        raise HTTPException(status_code=404, detail="Maratón no encontrado")
    
    db.delete(maraton_db)
    db.commit()
    return {"message": "Maratón eliminado con éxito"}

