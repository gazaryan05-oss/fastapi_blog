from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    posts_per_page: int = 10
    max_upload_size_bytes: int = 5 * 1024 * 1024

    database_url: str
    
    mail_server: str = "localhost"
    mail_port: int = 1025
    mail_username: str = ""
    mail_password: SecretStr = SecretStr("")
    mail_from: str = "noreply@example.com"
    mail_use_tls: bool = False
    
    frontend_url: str = "http://localhost:8000"
    reset_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()