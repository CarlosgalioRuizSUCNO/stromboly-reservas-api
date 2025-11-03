from fastapi import FastAPI
from src.app.api.v1 import rooms as rooms_router
from src.app.api.v1 import customers as customers_router
from src.app.api.v1 import bookings as bookings_router  # <-- NUEVO

# 🔹 Inicialización de la app
app = FastAPI(
    title="Stromboly Reservas API",
    version="0.1.0",
    description="API REST para gestionar reservas del Hotel Stromboly.",
)

# 🔹 Crear las tablas en el arranque
from src.app.db.session import engine
from src.app.db.base import Base

@app.on_event("startup")
def init_db():
    Base.metadata.create_all(bind=engine)

# 🔹 Endpoint de salud
@app.get("/health")
def health():
    return {"status": "ok"}

# 🔹 Rutas principales
app.include_router(rooms_router.router, prefix="/rooms", tags=["rooms"])
app.include_router(customers_router.router, prefix="/customers", tags=["customers"])
app.include_router(bookings_router.router, prefix="/bookings", tags=["bookings"])  # <-- NUEVO

# 🔹 Ejecución local (solo si corres con uvicorn manualmente)
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("APP_PORT", "8080"))
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=port)