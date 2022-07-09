from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_name: str
    database_username: str
    database_password: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_access_token_expiry_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
