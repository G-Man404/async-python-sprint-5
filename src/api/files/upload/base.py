import aiofiles
from fastapi import APIRouter, Depends
from fastapi import UploadFile

from src.api.auth.base import get_current_user
from src.db.db import add_file
from src.models.users import Users
from src.db.db import get_all_user_file

router_files_upload = APIRouter()


@router_files_upload.post('/')
async def create_upload_file(file: UploadFile, path: str, current_user: Users = Depends(get_current_user)):
    if path[-1] == "/":
        path += file.filename
    file_size = 0
    async with aiofiles.open(path, 'wb') as out_file:
        content = await file.read()
        file_size = len(content)
        await out_file.write(content)
    await add_file(file.filename, path, file_size, current_user)
    file_info = await get_all_user_file(current_user)
    return file_info[-1]
