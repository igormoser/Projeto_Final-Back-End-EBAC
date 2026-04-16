from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Pokemon API"
    app_version: str = "2.0.0"
    app_description: str = "API integradora da PokeAPI para o projeto final EBAC."
    database_url: str = "postgresql+psycopg://pokemon_user:pokemon_password@db:5432/pokemon_db"
    pokeapi_base_url: str = "https://pokeapi.co/api/v2"
    cache_ttl_minutes: int = 60
    request_timeout_seconds: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
