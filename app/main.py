from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.competencias import router as competencias_router
from app.routes.problemas import router as problemas_router
from app.routes.avances import router as avances_router
from app.routes.premios import router as premios_router  # ✅ IMPORTACIÓN AQUÍ
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Mi API",
    version="1.0.0",
    description="API para gestionar autenticación, competencias, avances y problemas.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ✅ Inclusión de routers
app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
app.include_router(competencias_router, prefix="/competencias", tags=["Competencias"])
app.include_router(problemas_router, prefix="/problemas", tags=["Problemas"])
app.include_router(avances_router, prefix="/avances", tags=["Avances"])
app.include_router(premios_router, prefix="/premios", tags=["Premios"])

# ✅ Ruta de prueba
@app.get("/")

def root():
    
    
    return {"message": "API funcionando correctamente"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "auth/login",
                    "scopes": {},
                }
            },
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

