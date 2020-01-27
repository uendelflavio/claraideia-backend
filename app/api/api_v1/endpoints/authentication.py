from datetime import timedelta

from fastapi import (
    APIRouter, 
    Body, 
    Depends)
from starlette.exceptions import HTTPException
from starlette.status import ( 
    HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST
)
from fastapi.security import ( 
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm 
)
from ....core.config import ( 
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY
)
from ....core.jwt import  create_access_token,get_current_user_authorizer
from ....crud.shortcuts import check_free_username_and_email
from ....crud.user import ( 
    create_user,
    get_user_by_email
)
from ....db.mongodb import (
    AsyncIOMotorClient, 
    get_database
)
from ....models.user import (
    User, 
    UserInCreate, 
    UserInLogin, 
    UserInResponse
)

router = APIRouter()


@router.post(
    "/token",
    response_model=UserInResponse,
    tags=["authentication"]
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user_dict = fake_users_db.get(form_data.username)

    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@router.get(
    "/users/me",
    response_model=UserInResponse,
    tags=["authentication"]
)
async def read_users_me(
    user: UserInLogin = Body(..., embed=True), 
    current_user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    return current_user


@router.post(
    "/users/login",
    response_model=UserInResponse,
    tags=["authentication"]
)
async def login(
        user: UserInLogin = Body(..., embed=True), 
        db: AsyncIOMotorClient = Depends(get_database)
):
    dbuser = await get_user_by_email(db, user.email)
    if not dbuser or not dbuser.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"username": dbuser.username}, expires_delta=access_token_expires)    
    return UserInResponse(user=User(**dbuser.dict(), token=token))


@router.post(
    "/users",
    response_model=UserInResponse,    
    status_code=HTTP_201_CREATED,
    tags=["authentication"],
)
async def register(
        user: UserInCreate = Body(..., embed=True), 
        db: AsyncIOMotorClient = Depends(get_database)         
):
    await check_free_username_and_email(db, user.username, user.email)
    dbuser = await create_user(db, user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)            
    token = create_access_token(data={"username": dbuser.username}, expires_delta=access_token_expires)                        
    return UserInResponse(user=User( **dbuser.dict(), token=token ))