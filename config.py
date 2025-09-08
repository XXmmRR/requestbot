from decouple import config
from typing import List
from pydantic import BaseModel, validator


class Settings(BaseModel):
    """Config files for bot."""

    TOKEN: str = config("TOKEN", default="")
    POSTGRES_DB: str = config("POSTGRES_DB", default="")
    POSTGRES_USER: str = config("POSTGRES_USER", default="")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="")
    DB_HOST: str = config("DB_HOST", default="localhost")
    DB_PORT: str = config("DB_PORT", default="5432")
    REDIS_HOST: str = config("REDIS_HOST", default="redis")
    admin_list: List[int] = []

    @validator("admin_list", pre=True)
    def parse_admin_list(cls, v):
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        return v


CONFIG = Settings(admin_list=config("ADMIN_LIST", default=""))
