from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models.database import engine
from .models.entities import Base
from .api import auth, ventas, inventario, entregas

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PoliMarket API",
    description="API para el sistema de gestión de PoliMarket",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(ventas.router)
app.include_router(inventario.router)
app.include_router(entregas.router)

@app.get("/")
def read_root():
    return {
        "message": "PoliMarket API funcionando",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth",
            "ventas": "/ventas", 
            "inventario": "/inventario",
            "entregas": "/entregas"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"} 