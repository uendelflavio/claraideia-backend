from typing import Optional
from pydantic import EmailStr, AnyUrl, ValidationError
from ..models.dbmodel import DBModelMixin
from ..models.rwmodel import RWModel
from ..core.security import generate_salt, get_password_hash, verify_password
# from ..core.security import generate_salt, get_password_hash, verify_password


    
    
class UserBase(RWModel):
    username: str
    email: EmailStr
    bio: Optional[str] = None

class User(UserBase):
    token: str

class UserInResponse(RWModel):
    user: User

# class UserInDB(DBModelMixin, UserBase):
#     salt: str = ""
#     hashed_password: str = ""
#     def check_password(self, password: str):
#         return verify_password(self.salt + password, self.hashed_password)

#     def change_password(self, password: str):
#         self.salt = generate_salt()
#         self.hashed_password = get_password_hash(self.salt + password)
        
        
class UserInDB(UserBase):
    # type: str = USERPROFILE_DOC_TYPE
    hashed_password: str
    username: str


class UserInLogin(RWModel):
    email: EmailStr
    password: str


class UserInCreate(DBModelMixin,UserInLogin):
    username: str


class UserInUpdate(RWModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[AnyUrl] = None

