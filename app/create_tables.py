from database import Base, engine
from models import usuarios, competencias, problemas, avances, premios  # Importa todos tus modelos
print("Creando las tablas si no existen...")
Base.metadata.create_all(bind=engine)
print("¡Tablas creadas correctamente!")
