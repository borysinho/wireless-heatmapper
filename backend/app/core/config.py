from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Base de datos
    database_url: str = "postgresql://heatmapper_user:password@db:5432/heatmapper"

    # Seguridad JWT
    secret_key: str = "cambia_esto_por_un_secreto_seguro"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # Servidor
    debug: bool = False
    cors_origins: list[str] = ["http://localhost", "http://localhost:5173"]

    @field_validator("debug", mode="before")
    @classmethod
    def normalizar_debug(cls, valor: object) -> object:
        if isinstance(valor, str) and valor.strip().lower() in {
            "release",
            "prod",
            "production",
        }:
            return False
        return valor

    # Storage de planos (Sprint 2)
    storage_root: str = "/var/lib/heatmapper/planos"
    storage_url_secret: str = "cambia_esto_secreto_para_firmar_urls"
    storage_url_ttl_seconds: int = 3600  # 1 hora
    # Prefijo opcional para URLs firmadas (e.g. "http://host/api"). Si vacío
    # se devuelven URLs relativas que el cliente concatena con su base.
    public_api_url: str = ""

    # Firebase Admin SDK (notificaciones de asignación de proyectos)
    firebase_project_id: str = ""
    firebase_credentials_path: str = ""
    firebase_credentials_json: str = ""

    # Correo transaccional (cuentas creadas y enlaces de cliente)
    email_notifications_enabled: bool = False
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_use_tls: bool = True
    smtp_timeout_seconds: int = 10
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_from_name: str = "Wireless HeatMapper"
    public_web_url: str = ""


settings = Settings()
