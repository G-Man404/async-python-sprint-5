from fastapi import APIRouter

from src.core.security import pwd_context, create_jwt_token, oauth2_scheme, verify_jwt_token
from src.db.db import find_user_by_name
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

router_auth = APIRouter()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await find_user_by_name(decoded_data["sub"])
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user


@router_auth.post('/')
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await find_user_by_name(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    is_password_correct = pwd_context.verify(form_data.password, user.hash_password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    jwt_token = create_jwt_token({"sub": user.name})
    return {"access_token": jwt_token, "token_type": "bearer"}

