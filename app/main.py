from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routes import auth
from app.routes.competencias import router as competencias_router
from app.routes.problemas import router as problemas_router
from app.routes.avances import router as avances_router
from app.routes.premios import router as premios_router  # ✅ IMPORTACIÓN AQUÍ

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(competencias_router, prefix="/competencias", tags=["Competencias"])
app.include_router(problemas_router, prefix="/problemas", tags=["Problemas"])
app.include_router(avances_router, prefix="/avances", tags=["Avances"])
app.include_router(premios_router, prefix="/premios", tags=["Premios"])  # ✅ REGISTRADO AQUÍ

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}

# 🔄 Forzar regeneración de OpenAPI
def custom_openapi():
    app.openapi_schema = None  # 🔥 ELIMINA CACHÉ DE OpenAPI
    openapi_schema = get_openapi(
        title="Mi API",
        version="1.0.0",
        description="API para gestionar autenticación, competencias, avances y problemas.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi  # ✅ RECARGA OpenAPI
