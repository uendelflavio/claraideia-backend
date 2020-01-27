import jwt
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN

from app import crud
from app.core import config
from app.core.jwt import ALGORITHM
# from app.db.database import get_default_bucket
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.token import TokenPayload
from app.models.user import UserInDB
from app.crud.user import get_user,is_active

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


def get_current_user(
    token: str = Security(reusable_oauth2),
    conn: AsyncIOMotorClient = Depends(get_database),
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )  
    # user = get_user(conn, username=token_data.username)
    user = get_user(conn, username=token_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: UserInDB = Security(get_current_user),
    conn: AsyncIOMotorClient = Depends(get_database),
):
    if not is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: UserInDB = Security(get_current_user)
):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
