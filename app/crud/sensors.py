from datetime import datetime
from typing import ( 
    Optional,
    List
)

from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from ..crud.user import get_user
from ..db.mongodb import AsyncIOMotorClient
from ..core.config import ( 
    database_name,
    sensors_collection_name 
)
from ..models.sensors import ( 
    Sensors,
    SensorsInDB,
    SensorsInCreate,
    SensorsInUpdate,
    SensorsList,
)
from bson.objectid import ObjectId


async def getSensor(
    conn: AsyncIOMotorClient,
    id: str
) -> SensorsInDB:
    row = await conn[database_name][sensors_collection_name].find_one({"_id": ObjectId(id)})
    if row:
        row['id'] = str(row['_id'])
        row.pop('_id', None)
        return row
        

async def fetchSensors(
    conn: AsyncIOMotorClient
) -> List[SensorsInDB]:
    sensors = []
    rows =  conn[database_name][sensors_collection_name].find({})
    async for row in rows:
        row['id'] = str(row['_id'])
        sensors.append(SensorsInDB(**row))        
    return sensors    

async def createSensor(
    conn: AsyncIOMotorClient, 
    sensors: SensorsInCreate,
) -> SensorsInDB: 
    sensors_doc = sensors.dict()
    sensors_doc['createdAt'] = datetime.now()
    sensors_doc['updatedAt'] = datetime.now()    
    row = await conn[database_name][sensors_collection_name].insert_one(sensors_doc)
    sensors_doc['id'] = str(ObjectId(row.inserted_id))
    
    return SensorsInDB(
        **sensors_doc
    )  

async def updateSensor(
    conn: AsyncIOMotorClient, 
    id: str, 
    sensors: SensorsInUpdate
) -> SensorsInDB:
    sensors_doc = await getSensor(conn, id)
    sensors_doc["description"] = sensors.description
    sensors_doc["data_reading"] = datetime.strptime(sensors.data_reading, '%Y-%m-%dT%H:%M:%S.%fZ')
    sensors_doc["reading"] = datetime.strptime(sensors.reading, '%Y-%m-%dT%H:%M:%S.%fZ') 
    sensors_doc['updatedAt'] = datetime.now()
    update_at = await conn[database_name][sensors_collection_name].update_one({"_id": ObjectId(id)}, {'$set': sensors_doc})
    sensors_doc["update_at"] = update_at
    return sensors_doc

 

async def deleteSensor(
    conn: AsyncIOMotorClient, 
    id: str
):
    delete_at = await conn[database_name][sensors_collection_name].delete_one({ "_id": ObjectId(id)})
    return delete_at
        
    
    
