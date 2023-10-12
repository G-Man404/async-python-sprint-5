import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordBearer


from core import config
from api.ping.base import router_get_ping
from api.auth.base import router_auth
from api.files.base import router_files
from api.files.download.base import router_files_download
from api.files.upload.base import router_files_upload
from api.register.base import router_register
from sys import argv

from db.db import create_model

app = FastAPI(
    title=config.app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(router_get_ping, prefix="/ping")
app.include_router(router_register, prefix="/register")
app.include_router(router_auth, prefix="/auth")
app.include_router(router_files, prefix="/files")
app.include_router(router_files_upload, prefix="/files/upload")
app.include_router(router_files_download, prefix="/files/download")

if __name__ == '__main__':
    if len(argv) > 0 and argv[0] == "db":
        asyncio.run(create_model())

    uvicorn.run(
        'main:app',
        host=config.app_settings.redis_host,
        port=config.app_settings.redis_port,
    )
