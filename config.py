from decouple import config
from typing import List
from pydantic import BaseModel, validator

class Settings(BaseModel):
    """Config files for bot."""

    TOKEN: str = config("TOKEN", default="")
    DB_NAME: str = config("DB_NAME", default="")
    DB_PORT: str = config("DB_PORT", default="")
    DB_PASSWORD: str = config("DB_PASSWORD", default="")
    DB_URL: str = config("DB_URL", default="")
    DB_USER: str = config("DB_USER", default="")
    
    admin_list: List[int] = []

    @validator('admin_list', pre=True)
    def parse_admin_list(cls, v):
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(',') if x.strip()]
        return v

CONFIG = Settings(admin_list=config("ADMIN_LIST", default=""))
