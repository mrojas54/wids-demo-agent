import os
import logging
import pathlib
from functools import lru_cache

from pydantic_settings import BaseSettings


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = bool(0)
    database_url: str = None
    openai_api_key: str = None


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()


class BaseConfig(BaseSettings):
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent

    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3"
    )
    DATABASE_CONNECT_DICT: dict = {}


class TestingConfig(BaseConfig):
    DEBUG: bool = True


class LocalConfig(BaseConfig):
    DEBUG: bool = True


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True


class StagingConfig(BaseConfig):
    DEBUG: bool = False


class ProductionConfig(BaseConfig):
    DEBUG: bool = False


@lru_cache
def get_config() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    config_cls_dict = {
        "development": DevelopmentConfig,
        "local": LocalConfig,
        "staging": StagingConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    config_name = os.environ.get("ENV", "local")
    config_cls = config_cls_dict[config_name]
    return config_cls()
