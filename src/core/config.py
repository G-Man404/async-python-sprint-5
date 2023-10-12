from pydantic import BaseSettings, PostgresDsn, Field
from logging import config as logging_config
from core.logger import LOGGING
import os


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

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/../.env"


app_settings = AppSettings()
