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
    users_collection_name 
)
from ..models.users import ( 
    UserInCreate, 
    UserInDB, 
    UserInUpdate
)
from bson.objectid import ObjectId