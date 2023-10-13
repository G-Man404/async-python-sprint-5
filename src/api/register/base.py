from fastapi import APIRouter

from fastapi import Request

from core.security import pwd_context
from db.db import ping_database, find_user_by_name, create_user
from fastapi.responses import Response

router_register = APIRouter()


@router_register.post('/')
async def register(request: Request, name, password):
    user = await find_user_by_name(name)
    if user is not None:
        return Response(status_code=401)
    await create_user(name, pwd_context.hash(password))
    return Response(status_code=201)
