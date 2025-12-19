from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV: str = "development"
    PROJECT_NAME: str = "DesignerCEP Backend"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./designercep.db"
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    
    ALLOWED_ORIGINS: str = "*"
    ADMIN_TOKEN: str = "admin-token"

    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "ly1104803132@gmail.com"
    SMTP_PASSWORD: str = "wsfrpnmkojpsqdkk"
    EMAILS_FROM_EMAIL: str = "ly1104803132@gmail.com"
    EMAILS_FROM_NAME: str = "Designer"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
