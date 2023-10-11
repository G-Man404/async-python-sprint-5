from os import path
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn, Field
from logging import config as logging_config
from src.core.logger import LOGGING
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

logging_config.dictConfig(LOGGING)

db_echo_mode = True

SECRET_KEY = "frgwergewrgerge"

class AppSettings(BaseSettings):
    app_title: str = "Title"
    database_dsn: PostgresDsn
    project_name: str = 'Some project name'
    redis_host: str = ...
    redis_port: int = ...
    elastic_host: str = Field(..., env='ELASTIC_HOST_NAME')
    elastic_port: int = Field(9200, env='ELASTIC_PORT')


app_settings = AppSettings()
