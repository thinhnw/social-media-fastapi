from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_url: str
    database_connection_str: str
    testdb_connection_str: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256" 
    jwt_token_ttl: int = 60 * 60
    tz: str = "UTC"
    pgtz: str = "UTC"

    class Config:
        env_file = ".env"


settings = Settings()

