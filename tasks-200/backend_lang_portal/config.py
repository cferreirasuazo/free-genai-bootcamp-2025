from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI App"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    class Config:
        env_file = ".env"

settings = Settings() 