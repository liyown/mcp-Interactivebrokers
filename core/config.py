from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    # IB TWS 连接设置
    TWS_HOST: str = "127.0.0.1"
    TWS_PORT: int = 7497
    TWS_CLIENT_ID: int = 1

    # API 服务器设置
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 1200
    API_ROOT_PATH: str = "/ib_api"

    # 日志设置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = "logs/ib_api.log"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
