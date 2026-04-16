from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Pokemon API"
    app_version: str = "1.0.0"
    app_description: str = "API final do curso EBAC inspirada na PokéAPI."
    database_url: str = "postgresql+psycopg://pokemon_user:pokemon_password@db:5432/pokemon_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
