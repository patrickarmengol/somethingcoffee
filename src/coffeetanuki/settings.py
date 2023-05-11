from functools import lru_cache
from pydantic import BaseSettings, PostgresDsn, ValidationError, parse_obj_as


class DatabaseSettings(BaseSettings):
    """Configures the database for the application."""

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_prefix = "DB_"

    URL: PostgresDsn = parse_obj_as(
        PostgresDsn, "postgresql+asyncpg://myuser:mypass@localhost:5432/postgres"
    )


@lru_cache
def load_settings() -> tuple[DatabaseSettings]:
    try:
        db: DatabaseSettings = DatabaseSettings.parse_obj({})
    except ValidationError as e:
        print("Couldn't load settings. %s", e)
        raise e from e
    return (db,)


(db,) = load_settings()
