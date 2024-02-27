from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App settings
    app_name: str = "SogoSign v1"
    app_description: str = "La aplicación de SogoSign API v1 - FastAPI"

    # Security settings
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()
