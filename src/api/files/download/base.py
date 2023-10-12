from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from api.auth.base import get_current_user
from models.users import Users
from db.db import get_file

router_files_download = APIRouter()


@router_files_download.post('/')
async def create_upload_file(s_path: str, current_user: Users = Depends(get_current_user)):
    file = await get_file(s_path)
    if not file:
        return "File not found"
    print(file)
    media_type = file.path.split(".")[-1]
    return FileResponse(path=file.path, filename=file.name, media_type=media_type)