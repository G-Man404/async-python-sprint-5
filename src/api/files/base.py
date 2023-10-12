from fastapi import APIRouter, Depends
from fastapi import Request

from api.auth.base import get_current_user
from db.db import get_all_user_file
from models.users import Users

router_files = APIRouter()


@router_files.post('/')
async def get_files(request: Request, current_user: Users = Depends(get_current_user)):
    files = await get_all_user_file(current_user)
    return files
