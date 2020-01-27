
from typing import Optional

from fastapi import APIRouter, Depends, Path,Body
from starlette.exceptions import HTTPException
from starlette.status import ( 
    HTTP_422_UNPROCESSABLE_ENTITY, 
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

from ....core.jwt import get_current_user_authorizer
from ....crud.station import  ( 
    get_station, 
    create_station, 
    update_station
)
from ....db.mongodb import (
    AsyncIOMotorClient,
    get_database
)
from ....models.station import (
    StationInResponse,
    StationInCreate, 
    StationInUpdate
)
from ....models.user import User

router = APIRouter()

@router.get("/stations", 
    response_model=StationInResponse, 
    tags=["stations"],
)
async def get_station(
    descricao: str = Path(..., min_length=1),
    # user: Optional[User] = Depends(get_current_user_authorizer(required=False)),
    db: AsyncIOMotorClient = Depends(get_database),
):
    sensor = StationInResponse(sensor=sensor)
    return sensor


@router.post(
    "/stations",
    response_model=StationInResponse,
    tags=["stations"],
    status_code=HTTP_201_CREATED,
)
async def create_station(
        descricao: StationInCreate = Body(..., embed=True),
        # user: User = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database),
):
    dbsensor = await create_sensor(db, descricao, user.username)
    return create_aliased_response(SensorInResponse(sensor=dbsensor))




@router.put("/stations/{slug}", 
    response_model=StationInResponse, 
    tags=["stations"],
)
async def update_station(
        descricao: StationInUpdate = Body(..., embed=True),
        # user: User = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database),
):
    dbsensor = await update_sensor(db, slug, article, user.username)
    return create_aliased_response(StationInResponse(sensor=dbsensor))




@router.delete(
    "/stations/{slug}", 
    tags=["stations"], 
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_station(        
        # user: User = Depends(get_current_user_authorizer()),
        db: AsyncIOMotorClient = Depends(get_database),
):
    await delete_article_by_slug(db, slug, user.username)