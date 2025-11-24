from pydantic import BaseModel, EmailStr
from datetime import datetime

# Mô hình dữ liệu
class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    active: bool = True

class UserInDB(User):
    hashed_password: str
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserInfo(BaseModel):
    username: str
    email: EmailStr
    
class UserResponse(BaseModel):
    username: str
    email: EmailStr
    created_at: datetime
    active: bool
    
     # Xử lý ObjectId từ MongoDB
    class Config:
        orm_mode = True
    
class UserActive(BaseModel):
    email: EmailStr
    active: bool
    
class HomeForClient(BaseModel):
    id_comic: str
    switch: str
    
class HomeForClient(BaseModel):
    id_comic: str
    switch: str
    
class FavoriteForUser(BaseModel):
    id_comic: str
    email: EmailStr
    status: bool
    
class HistoryComicRequest(BaseModel):
    email: str
    id_comic: str
    chapter_name: str
    