
from typing import Optional

from fastapi import APIRouter, Depends, Path, Body
from starlette.exceptions import HTTPException
from starlette.status import ( 
    HTTP_422_UNPROCESSABLE_ENTITY, 
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)
from ....core.utils import create_aliased_response
from ....core.jwt import get_current_user_authorizer
from ....crud.sensors import ( 
    getSensor, 
    fetchSensors,
    createSensor, 
    updateSensor,
    deleteSensor
)
from ....db.mongodb import (
    AsyncIOMotorClient,
    get_database
)
from ....models.sensors import (
    Sensors,
    SensorsInDB,
    SensorsInResponse,
    SensorsInCreate, 
    SensorsInUpdate,
    SensorsList
)
from ....models.user import User

router = APIRouter()


@router.get(
    "/sensor/{id}",
    response_model=SensorsInResponse,    
    tags=["sensors"]
)
async def get_sensor(
    # user: Optional[User] = Depends(get_current_user_authorizer(required=False)),
    id: str = Path(..., min_length=1),
    db: AsyncIOMotorClient = Depends(get_database),
):
    sensor = await getSensor(db,id)
    return SensorsInResponse(sensors=SensorsInDB(**sensor))



@router.get(
    "/sensors",
    response_model=SensorsList,    
    tags=["sensors"]
)
async def get_all_sensor(
    # user: Optional[User] = Depends(get_current_user_authorizer(required=False)),
    db: AsyncIOMotorClient = Depends(get_database),
):
    sensors = await fetchSensors(db)
    return SensorsList(sensors=[sensor for sensor in sensors])


@router.post(
    "/sensor",
    response_model=SensorsInResponse,
    tags=["sensors"],
    status_code=HTTP_201_CREATED,
)
async def create_sensor(      
    sensor: SensorsInCreate =  Body(..., embed=True),
    db: AsyncIOMotorClient = Depends(get_database),
):
    dbsensor = await createSensor(db, sensor)
    return SensorsInResponse(sensors=Sensors(**dbsensor.dict()))  


@router.put(
    "/sensor/{id}", 
    response_model=SensorsInResponse,    
    tags=["sensors"],
)
async def update_sensor(    
    sensors: SensorsInUpdate = Body(..., embed=True),  
    id: str = Path(..., min_length=1),  
    db: AsyncIOMotorClient = Depends(get_database),
):
    dbsensor = await updateSensor(db, id, sensors) 
    return SensorsInResponse(sensors=Sensors(**dbsensor))



@router.delete(
    "/sensor/{id}", 
    tags=["sensors"]
)
async def delete_sensor(        
    id: str = Path(..., min_length=1),
    db: AsyncIOMotorClient = Depends(get_database),
):
    sensor = await deleteSensor(db, id)
    return {"status": f"deleted count: {sensor.deleted_count}"} 
    