from fastapi import APIRouter, Header, Depends
from fastapi import Response
from fastapi import Request

from src.api.auth.base import get_current_user
from src.db.db import get_files
from src.models.users import Users

router_files = APIRouter()


@router_files.post('/')
async def get_files(request: Request, current_user: Users = Depends(get_current_user)):
    print(current_user)
