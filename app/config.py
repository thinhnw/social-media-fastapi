from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_url: str
    postgres_user: str  
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_db: str
    @property
    def database_connection_str(self) -> str: 
        return (
            "postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    @property
    def testdb_connection_str(self) -> str: 
        return self.database_connection_str + "_test"

    jwt_secret_key: str
    jwt_algorithm: str = "HS256" 
    jwt_token_ttl: int = 60 * 60
    tz: str = "UTC"
    pgtz: str = "UTC"

    class Config:
        env_file = ".env"


settings = Settings()

