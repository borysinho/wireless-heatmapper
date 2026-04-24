from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="Wireless HeatMapper API",
    description="Backend REST + IA para el sistema de análisis de cobertura WiFi. Bulldog Tech.",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["infraestructura"])
def health_check():
    """Verifica que el backend esté operativo."""
    return {"status": "ok", "version": "0.1.0"}
