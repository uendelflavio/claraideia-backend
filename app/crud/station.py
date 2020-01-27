from typing import Optional

from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from ..crud.user import get_user
from ..db.mongodb import AsyncIOMotorClient
from ..core.config import database_name, station_collection_name
from ..models.station import Station,StationInDB, StationInCreate, StationInUpdate 


async def get_station(
        conn: AsyncIOMotorClient,
        target_username: str, 
        current_username: Optional[str] = None
    ) -> Station:
    user = await get_user(conn, target_username)
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"User {target_username} not found"
        )
    station = Station(**user.dict())
    station.following = await is_following_for_user(
        conn, current_username, target_username
    )
    return station


async def create_station(
        conn: AsyncIOMotorClient, 
        station: StationInCreate,
    ) -> StationInDB:
    dbstation = StationInDB(**station.dict())    
    dbstation.id = row.inserted_id
    dbstation.created_at = ObjectId(dbstation.id ).generation_time
    dbstation.updated_at = ObjectId(dbstation.id ).generation_time
    row = await conn[database_name][station_collection_name].insert_one(dbsensor.dict())
    return dbstation    



async def update_station(
        conn: AsyncIOMotorClient, 
        sensor: StationInUpdate
    ) -> StationInDB:
    dbstation = StationInUpdate(**sensor.dict())    
    dbstation.id = row.inserted_id
    dbstation.created_at = ObjectId(dbstation.id ).generation_time
    dbstation.updated_at = ObjectId(dbstation.id ).generation_time
    row = await conn[database_name][station_collection_name].update_one({"username": dbuser.username}, {'$set': dbsensor.dict()})
    return dbstation  

    

async def delete_sensor(conn: AsyncIOMotorClient, id: int, username: str):
    await conn[database_name][station_collection_name].delete_many({"id": id, "username": username})