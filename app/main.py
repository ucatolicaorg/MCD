from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.competencias import router as competencias_router  # Nueva importación

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(competencias_router, prefix="/competencias")  # Nueva ruta añadida

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
