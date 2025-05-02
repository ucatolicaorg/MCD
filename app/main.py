from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

# Rutas
from app.routes.auth import router as auth_router
from app.routes.competencias import router as competencias_router
from app.routes.problemas import router as problemas_router
from app.routes.avances import router as avances_router
from app.routes.premios import router as premios_router
from app.routes.resolver_problemas import router as resolver_problema_router
from app.routes.maratones import router as maratones_router  # <-- Aquí se agrega la ruta de maratones

# Crear la app de FastAPI
app = FastAPI(
    title="Mi API",
    version="1.0.0",
    description="API para gestionar autenticación, competencias, avances y problemas.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración CORS
origins = [
    "http://localhost",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite solicitudes de estos dominios
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)

# Incluir routers
app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
app.include_router(competencias_router, prefix="/competencias", tags=["Competencias"])
app.include_router(problemas_router, prefix="/problemas", tags=["Problemas"])
app.include_router(avances_router, prefix="/avances", tags=["Avances"])
app.include_router(premios_router, prefix="/premios", tags=["Premios"])
app.include_router(resolver_problema_router, prefix="/resolver", tags=["Resolver Problemas"])
app.include_router(maratones_router, prefix="/maratones", tags=["Maratones"])  # <-- Agregar este router para maratones

# Ruta principal
@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}

# Nuevo endpoint para el formulario de registro de usuario
class RegistroUsuario(BaseModel):
    nombre: str
    email: str
    password: str
    is_profesor: bool

@app.post("/registro")
def registrar_usuario(datos: RegistroUsuario):
    print(f"Datos recibidos: {datos}")
    return {"mensaje": f"Usuario {datos.nombre} registrado correctamente"}

# Configuración OpenAPI personalizada
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Aquí se configura la seguridad de OAuth2 para la API
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/login",  # URL de la ruta para obtener el token
                    "scopes": {},
                }
            },
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


