from typing import ( 
    Optional,
    List,
)

from pydantic import ( 
    AnyUrl,
    BaseModel 
)
from datetime import datetime
from ..models.dbmodel import DBModelMixin
from ..models.rwmodel import RWModel


# class Sensors(RWModel):
#     description: str
#     data_reading: datetime
#     reading: datetime
        
class SensorsInDB(DBModelMixin, RWModel):
    description: str
    data_reading: datetime
    reading: datetime

class Sensors(SensorsInDB):
    description: str
    data_reading: datetime
    reading: datetime


class SensorsInResponse(RWModel):
    sensors: Sensors



class SensorsInCreate(Sensors):
    pass


class SensorsInUpdate(RWModel):
    description: Optional[str] = None
    data_reading: Optional[str] = None
    reading: Optional[str] = None
    
    

class SensorsList(RWModel):
    sensors: List[SensorsInDB] = []